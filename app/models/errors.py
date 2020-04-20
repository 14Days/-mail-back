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
