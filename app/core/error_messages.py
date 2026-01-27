"""Error message constants"""


class ErrorMessages:
    """Class with error message constants"""

    # User errors
    USER_NOT_FOUND = "User not found"
    USER_ALREADY_EXISTS = "User with this email already exists"
    USER_INACTIVE = "User is inactive"

    # Admin errors
    ADMIN_NOT_FOUND = "Admin not found"
    ADMIN_INACTIVE = "Admin is inactive"

    # Authentication errors
    INVALID_CREDENTIALS = "Could not validate credentials"
    INCORRECT_EMAIL_OR_PASSWORD = "Incorrect email or password"

    # Payment errors
    INVALID_SIGNATURE = "Invalid signature"
    TRANSACTION_ALREADY_PROCESSED = "Transaction already processed"
    ACCOUNT_BELONGS_TO_ANOTHER_USER = "Account belongs to another user"

    # Account errors
    ACCOUNT_NOT_FOUND = "Account not found"
