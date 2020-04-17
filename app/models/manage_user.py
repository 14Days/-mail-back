class IManageUser:
    def get_all_user(self):
        pass

    def get_user_detail(self):
        pass

    def add_user(self, username: str, password: str):
        pass

    def modify_user(self, info: dict) -> None:
        pass

    def delete_user(self) -> None:
        pass


class ManageUser(IManageUser):
    user_id: str
    page: int
    limit: int

    def __init__(self, user_id=None, page=0, limit=10):
        self.user_id = user_id
        self.page = page
        self.limit = limit

    def get_all_user(self):
        pass

