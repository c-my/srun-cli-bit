import json
import logging
import time
from enum import Enum
from typing import Dict, Union
from urllib.parse import urlparse, parse_qs

import requests

from srunbit import model
from srunbit.encrypt import hash


class LoginCode(Enum):
    FAILED = 0
    SUCCESSFUL = 1
    ALREADY_ONLINE = 2
    ARREARAGE = 3
    WRONG_PASSWORD = 4
    USER_DISABLED = 5


class LogoutCode(Enum):
    FAILED = 0
    SUCCESSFUL = 1
    ALREADY_OFFLINE = 2


class Network:
    def __init__(self):
        self.__base_url = 'http://10.0.0.55'
        self.__challenge_url = "/cgi-bin/get_challenge"
        self.__portal_url = "/cgi-bin/srun_portal"
        self.__successful_url = "/cgi-bin/rad_user_info"

    def login(self, account: model.Account) -> LoginCode:
        try:
            ac_id = self._get_ac_id()[0]
        except Exception as e:
            logging.debug(f'get ac_id failed: {e}')
            return LoginCode.FAILED
        username = account.username
        password = account.password

        form_login = model.login(username, password, ac_id)
        try:
            challenge = self._get_challenge(username)
        except Exception as e:
            logging.debug(f'get challenge failed: {e}')
            return LoginCode.FAILED

        token = challenge['challenge']
        ip = challenge['client_ip']
        form_login['ip'] = ip
        form_login['info'] = hash.gen_info(form_login, token)
        form_login['password'] = hash.pwd_hmd5('', token)
        form_login['chksum'] = hash.checksum(form_login, token)
        try:
            json_obj = self._get_json(self.__base_url + self.__portal_url, form_login)
        except Exception as e:
            logging.debug(f'login failed: {e}')
            return LoginCode.FAILED
        if 'res' not in json_obj:
            logging.debug(f'field "res" not in json, got json: {json_obj}')
            return LoginCode.FAILED
        if json_obj['res'] != 'ok':
            error_msg = json_obj['error_msg']
            if 'Arrearage users' in error_msg:
                return LoginCode.ARREARAGE
            elif 'You are already online.' in error_msg:
                return LoginCode.ALREADY_ONLINE
            elif 'Password is error' in error_msg:
                return LoginCode.WRONG_PASSWORD
            elif 'User is disabled' in error_msg:
                return LoginCode.USER_DISABLED
            else:
                logging.debug(f'login res is not ok, got error_msg: {error_msg}')
                print(json_obj)
                return LoginCode.FAILED
        return LoginCode.SUCCESSFUL

    def logout(self, account: model.Account) -> LogoutCode:
        form_logout = model.logout(account.username)
        try:
            json_obj = self._get_json(self.__base_url + self.__portal_url, form_logout)
        except Exception as e:
            logging.debug(f'logout failed: {e}')
            return LogoutCode.FAILED
        if json_obj['error'] != 'ok':
            error_msg = json_obj['error_msg']
            if 'You are not online' in error_msg:
                return LogoutCode.ALREADY_OFFLINE
            else:
                return LogoutCode.FAILED
        return LogoutCode.SUCCESSFUL

    def get_info(self) -> Union[Dict, None]:
        try:
            json_obj = self._get_json(self.__base_url + self.__successful_url)
        except Exception as e:
            logging.debug(f'get info failed: {e}')
            return None
        return json_obj

    def _get_ac_id(self) -> str:
        r = requests.get(self.__base_url)
        d = urlparse(r.url)
        query = parse_qs(d.query)
        ac_id = query['ac_id'][0]
        return ac_id

    def _get_json(self, url: str, data=None):
        if data is None:
            data = {}
        r = self._request_with_callback(url, data)
        body = r.text
        s = body.find('(')
        e = body.rfind(')')
        body = body[s + 1:e]
        json_obj = json.loads(body)
        return json_obj

    def _get_challenge(self, username: str) -> dict:
        params = {
            'username': username,
            'ip': '',
        }
        return self._get_json(self.__base_url + self.__challenge_url, params)

    def _request_with_callback(self, url: str, params: dict):
        params['callback'] = self._gen_callback()
        params['_'] = self._gen_callback()
        r = requests.get(url, params=params)
        return r

    def _gen_callback(self) -> str:
        return f'{int(time.time() * 1000)}'
