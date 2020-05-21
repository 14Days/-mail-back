from app.models.email.IEmail import IEmail
from app.models.email.AdminEmail import AdminEmail
from app.models.email.UserEmail import UserEmail

__all__ = ['get_email']


def get_email(user_type: int, user_id=None, subject=None, page=0, limit=10) -> IEmail.__class__:
    if user_type == 1:
        return AdminEmail(user_id=user_id, page=page, limit=limit, subject=subject)
    else:
        return UserEmail(user_id=user_id, page=page, limit=limit, subject=subject)
