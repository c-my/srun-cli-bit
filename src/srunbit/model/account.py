from typing import Dict


class Account:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.access_token = ""
        self.acid = ""

    def to_dict(self):
        return {"username": self.username, "password": self.password}

    @classmethod
    def from_dict(cls, data: Dict):
        return Account(data["username"], data["password"])
