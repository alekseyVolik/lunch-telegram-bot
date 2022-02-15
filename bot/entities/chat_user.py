class ChatUser:

    @classmethod
    def create_from_dict(cls, attributes):
        return cls(**attributes)

    def __init__(self, _id, _first_name, _last_name, _check_in, _status):
        self._id = _id
        self._first_name = _first_name
        self._last_name = _last_name
        self._check_in = _check_in
        self._status = _status

    def get_user_id(self):
        return self._id

    def set_user_id(self, _id):
        self._id = _id

    def get_user_name(self):
        return f"{self._first_name} {self._last_name}"

    def set_user_name(self, _first_name, _last_name):
        self._first_name = _first_name
        self._last_name = _last_name

    def get_check_in(self):
        return self._check_in

    def set_check_in(self, _check_in):
        self._check_in = _check_in

    def get_status(self):
        return self._status

    def set_status(self, _status):
        self._status = _status

    def attribute_as_dict(self):
        return {attribute: getattr(self, attribute) for attribute in self.__dict__ if attribute.startswith('_')}

    def __str__(self):
        return f"{self.__class__.__name__} {self.get_user_name()} with id {self.get_user_id()}"
