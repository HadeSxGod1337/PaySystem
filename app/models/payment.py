from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class Payment(Base):
    """Payment model (balance top-up)"""

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    amount = Column(Numeric(10, 2, asdecimal=True), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="payments")

    # transaction_id uniqueness is guaranteed at DB level
    __table_args__ = (UniqueConstraint("transaction_id", name="uq_payment_transaction_id"),)
