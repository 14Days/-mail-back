class UserNotFound(Exception):
    pass


class PasswordError(Exception):
    pass


class UserHaveExist(Exception):
    pass


class PasswordNotSatisfactory(Exception):
    pass


class DeleteAdminError(Exception):
    pass


class PropertyNotExist(Exception):
    pass


class ModifyAdminError(Exception):
    pass


class ModifyUserTypeError(Exception):
    pass


class AddressError(Exception):
    pass


class AddressExist(Exception):
    pass


class AddressNotExist(Exception):
    pass


class MailNotExist(Exception):
    pass


class NotYourMail(Exception):
    pass


class AddrIsUseless(Exception):
    pass


class UserIsUseless(Exception):
    pass


class HaveNoReceiver(Exception):
    pass


class PortOutOfRange(Exception):
    pass


class StateNotExist(Exception):
    pass


class SMTPServerUseless(Exception):
    pass


class POPServerUseless(Exception):
    pass
