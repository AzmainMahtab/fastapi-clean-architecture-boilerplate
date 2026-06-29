class UserAlreadyExistsError(Exception):
    """BUSINESS EXCEPTION:
    User with the given email or username already exists.
    """

    pass


class UserNotFoundError(Exception):
    """
    BAD REQUEST EXCEPTION:
    User with the given identifier (email, username, or ID) was not found.
    """

    pass


class InvalidCredentialsError(Exception):
    """
    BAD REQUEST EXCEPTION:
    Given credentials (email/username and password) are invalid.
    """

    pass


class InvalidOTPError(Exception):
    """
    BAD REQUEST EXCEPTION:
    Given OTP code is invalid or has expired.
    """

    pass


class CannotUpdateToInactiveError(Exception):
    pass


class UserNotDeletedError(Exception):
    pass


class PasswordsDoNotMatchError(Exception):
    pass


class WeakPasswordError(Exception):
    pass


class InvalidPhoneNumberError(Exception):
    pass
