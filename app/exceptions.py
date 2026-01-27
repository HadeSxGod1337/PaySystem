"""Custom exceptions for application"""

from typing import Optional

from fastapi import status


class BaseAppException(Exception):
    """Base application exception"""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: Optional[str] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.detail = detail or message
        super().__init__(self.message)


class NotFoundError(BaseAppException):
    """Exception for resources that are not found"""

    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class BadRequestError(BaseAppException):
    """Exception for incorrect requests"""

    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UnauthorizedError(BaseAppException):
    """Exception for unauthorized requests"""

    def __init__(self, message: str, detail: Optional[str] = None, headers: Optional[dict] = None):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
        self.headers = headers or {"WWW-Authenticate": "Bearer"}


class ForbiddenError(BaseAppException):
    """Exception for forbidden operations"""

    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN, detail=detail)


# Специфичные исключения для домена


class UserNotFoundError(NotFoundError):
    """Пользователь не найден"""

    pass


class UserAlreadyExistsError(BadRequestError):
    """Пользователь уже существует"""

    pass


class UserInactiveError(ForbiddenError):
    """Пользователь неактивен"""

    pass


class AdminNotFoundError(NotFoundError):
    """Администратор не найден"""

    pass


class AdminInactiveError(ForbiddenError):
    """Администратор неактивен"""

    pass


class InvalidCredentialsError(UnauthorizedError):
    """Неверные учетные данные"""

    pass


class IncorrectEmailOrPasswordError(UnauthorizedError):
    """Неверный email или пароль"""

    pass


class InvalidSignatureError(BadRequestError):
    """Неверная подпись"""

    pass


class TransactionAlreadyProcessedError(BadRequestError):
    """Транзакция уже обработана"""

    pass


class AccountBelongsToAnotherUserError(BadRequestError):
    """Счет принадлежит другому пользователю"""

    pass


class AccountNotFoundError(NotFoundError):
    """Счет не найден"""

    pass
