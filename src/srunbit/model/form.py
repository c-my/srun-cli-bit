from typing import Dict


def login(username: str, password: str, acid: str) -> Dict:
    return {
        'action': 'login',
        'username': username,
        'password': password,
        'ac_id': acid,
        'ip': '',
        'info': '',
        'chksum': '',
        'n': '200',
        'type': '1'
    }


def logout(username: str) -> Dict:
    return {
        'action': 'logout',
        'username': username,
    }
