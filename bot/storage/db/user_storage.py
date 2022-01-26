class UserStorage:

    _storage = {}

    def __init__(self):
        print('Create new instance')

    def add_user(self, _id: int, info: dict) -> None:
        self._storage[_id] = info

    def update_user(self, _id: int, info: dict) -> None:
        self._storage[_id] = info

    def get_user(self, _id: int) -> dict:
        return self._storage.get(_id, None)

    def get_users_list(self):
        return self._storage.values()
