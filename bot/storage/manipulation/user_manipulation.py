from bot.storage.db.user_storage import UserStorage


def add_user(storage: UserStorage, user_info: dict):
    user_id = user_info['_id']
    storage.add_user(_id=user_id, info=user_info)


def get_user_by_id(storage: UserStorage, user_id: int):
    return storage.get_user(_id=user_id)


def update_check_in_status(storage: UserStorage, user_id: int, status: bool):
    user_info = storage.get_user(_id=user_id)
    user_info['check_in'] = status
    storage.update_user(_id=user_id, info=user_info)


def update_status(storage: UserStorage, user_id: int, status: bool):
    user_info = storage.get_user(_id=user_id)
    user_info['status'] = status
    storage.update_user(_id=user_id, info=user_info)


def get_signed_user(storage: UserStorage) -> list:
    return [user for user in storage.get_users_list() if user['status'] is True]
