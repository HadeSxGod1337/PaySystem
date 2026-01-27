from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.error_messages import ErrorMessages
from app.core.security import verify_signature
from app.exceptions import (
    AccountBelongsToAnotherUserError,
    InvalidSignatureError,
    TransactionAlreadyProcessedError,
    UserNotFoundError,
)
from app.models.account import Account
from app.models.payment import Payment
from app.repositories.account_repository import AccountRepository
from app.repositories.payment_repository import PaymentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.payment import WebhookRequest
from app.services.service import Service


class PaymentService(Service[Payment]):
    """Service for working with payments"""

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.payment_repo = PaymentRepository()
        self.account_repo = AccountRepository()
        self.user_repo = UserRepository()

    async def _verify_signature(self, webhook_data: WebhookRequest) -> None:
        """Verify webhook signature"""
        data_dict = {
            "account_id": webhook_data.account_id,
            "amount": str(webhook_data.amount),
            "transaction_id": webhook_data.transaction_id,
            "user_id": webhook_data.user_id,
        }

        if not verify_signature(data_dict, webhook_data.signature, settings.webhook_secret_key):
            raise InvalidSignatureError(
                message=ErrorMessages.INVALID_SIGNATURE, detail=ErrorMessages.INVALID_SIGNATURE
            )

    async def _check_transaction_uniqueness(self, transaction_id: str) -> None:
        """Check transaction uniqueness"""
        existing_payment = await self.payment_repo.get_by_transaction_id(self.db, transaction_id)
        if existing_payment:
            raise TransactionAlreadyProcessedError(
                message=ErrorMessages.TRANSACTION_ALREADY_PROCESSED,
                detail=ErrorMessages.TRANSACTION_ALREADY_PROCESSED,
            )

    async def _get_or_create_account(self, user_id: int, account_id: int) -> Account:
        """Get existing account or create new one"""
        # Check if account exists for user with this account_id
        account = await self.account_repo.get_by_user_and_account_id(self.db, user_id, account_id)

        if account:
            return account

        # Check if this account_id belongs to another user
        existing_account = await self.account_repo.get_by_id(self.db, account_id)
        if existing_account and existing_account.user_id != user_id:
            raise AccountBelongsToAnotherUserError(
                message=ErrorMessages.ACCOUNT_BELONGS_TO_ANOTHER_USER,
                detail=ErrorMessages.ACCOUNT_BELONGS_TO_ANOTHER_USER,
            )

        # If account with this ID doesn't exist, create new one
        if not existing_account:
            account = await self.account_repo.create(
                self.db, user_id, initial_balance=Decimal("0.00"), account_id=account_id
            )
        else:
            # If account exists and belongs to this user, use it
            account = existing_account

        return account

    async def _process_payment(
        self, transaction_id: str, user_id: int, account: Account, amount: Decimal
    ) -> Payment:
        """Create payment and update account balance"""
        # Save transaction
        account_id: int = int(account.id)
        payment = await self.payment_repo.create(
            self.db, transaction_id, user_id, account_id, amount
        )

        # Add amount to account
        await self.account_repo.update_balance(self.db, account, amount)

        return payment

    async def process_webhook(self, webhook_data: WebhookRequest) -> dict:
        """Process webhook from payment system"""
        # Verify signature
        await self._verify_signature(webhook_data)

        # Check transaction uniqueness
        await self._check_transaction_uniqueness(webhook_data.transaction_id)

        # Check if user exists
        user = await self.user_repo.get_by_id(self.db, webhook_data.user_id)
        if not user:
            raise UserNotFoundError(
                message=ErrorMessages.USER_NOT_FOUND, detail=ErrorMessages.USER_NOT_FOUND
            )

        # Get or create account
        account = await self._get_or_create_account(webhook_data.user_id, webhook_data.account_id)

        # Process payment
        amount = webhook_data.amount
        payment = await self._process_payment(
            webhook_data.transaction_id, webhook_data.user_id, account, amount
        )

        # Refresh balance to get actual value
        await self.db.refresh(account)

        return {
            "message": "Payment processed successfully",
            "payment_id": payment.id,
            "account_id": account.id,
            "new_balance": account.balance,
        }

    async def get_user_payments(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Payment]:
        """Get all user payments"""
        payments = await self.payment_repo.get_by_user_id(self.db, user_id, skip, limit)
        return payments
