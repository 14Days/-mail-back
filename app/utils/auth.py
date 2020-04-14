from functools import wraps
from flask import g
from app.utils.errors import errors
from app.utils.warp import fail_warp


class Permission:
    """
    用户角色枚举类
    """
    ADMIN = 0x1
    NORMAL = 0x2

    ROLE_MAP = {
        1: 0x1,
        2: 0x2,
    }


def auth_require(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_role = g.user_type
            if Permission.ROLE_MAP[int(user_role)] & role != Permission.ROLE_MAP[int(user_role)]:
                return fail_warp(403, errors['403']), 401
            return func(*args, **kwargs)

        return wrapper

    return decorator
