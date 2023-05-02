import enum
import json
import re
import random
from typing import Union
import requests
import base64
import urllib.parse
from classes import VKUserPC

DEFAULT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 " \
             "Safari/537.36 "


class JsonSerializable:
    @classmethod
    def from_json(cls, json_data):
        object_ = json.loads(json_data, object_hook=lambda d: cls(**d))
        return object_

    def to_json(self):
        json_object = json.dumps(self.__dict__)
        return json_object


class AuthException(Exception):
    CAPTCHA_NEEDED = 'Captcha needed'
    REG_NEEDED = 'Registration needed'
    LEGACY_BAD_REQUEST = "Bad Legacy Request"

    def __init__(self, error, json_data: Union[dict, str] = None):
        if isinstance(json_data, str):
            json_data = json.loads(json_data)

        self.message = error
        super().__init__(self.message)

        self.data = json_data


class VKIDException(Exception):
    CAPTCHA_NEEDED = 14

    def __init__(self, json_data: Union[dict, str]):
        if isinstance(json_data, str):
            json_data = json.loads(json_data)

        self.code = json_data['error']['error_code']
        self.error_msg = json_data['error']['error_msg']

        self.message = f"[{self.code}] {self.error_msg}"
        super().__init__(self.message)

        self.data = json_data


class VKIDResponseHandle:
    def __init__(self, json_data: Union[dict, str]):
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
        if 'error' in json_data:
            raise VKIDException(json_data)
        elif 'response' in json_data:
            self.data = json_data['response']


class LegacyResponseHandle:
    def __init__(self, json_data: Union[dict, str]):
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
        if 'type' in json_data and json_data['type']=='error':
            raise AuthException(AuthException.LEGACY_BAD_REQUEST, json_data)
        elif 'type' in json_data and json_data['type']=='okay':
            self.data = json_data['data']


class VKIDAuth:

    class LoginType(enum.Enum):
        email = 'email'
        phone = 'phone'

    class FlowName(enum.Enum):
        need_password_and_validation = "need_password_and_validation"
        need_registration = "need_registration"
        need_password = "need_password"

    def __init__(self, login, password, useragent: str = None):
        self.session = requests.session()
        self.session.headers['User-Agent'] = useragent if useragent is not None else DEFAULT_UA
        self.login = login
        self.password = password

    def _generate_uuid(self):
        return ''.join(random.sample("28SabBruMmWeys-ARE_F4cK1NgVkZXCOwndlohP035679DGHftiUvzqYTJLxpIjQ", 21))

    def _parse_params(self):

        # парс хэша с главной страницы вк
        RE_PARSE_HASH = re.compile(r'initVkId.*"hash":"(\w*)"')
        resp = self.session.get('https://vk.com/')
        self.hash = RE_PARSE_HASH.findall(resp.text)[0]

    def _auth_page_login(self, login):

        RE_PARSE_ANON = re.compile(
            r'window\.init.*"access_token":"([28SabBruMmWeys\-ARE_F4cK1NgVkZXCOwndlohP035679DGHftiUvzqYTJLxpIjQ.]*)"'
        )

        # Ajax-запрос для формирования аутентификации
        resp = self.session.post("https://vk.com/join.php?act=connect", params={
            'al': '1',
            'expire': '0',
            'hash': self.hash,
            'login': login,
            'save_user': '1'
        }, headers={
            "origin":"https://vk.com",
            "referer":"https://vk.com/",

        })
        resp = json.loads(resp.text.replace("<!--", ""))

        action = {
            "name": "no_password_flow",
            "token": resp['payload'][1][1],
            "params": {
                "type": "sign_in",
                "csrf_hash": self.hash
            }
        }
        initial_stats_info = {
            "source": "main",
            "screen": "start"
        }
        vkid_url = f"https://id.vk.com/auth?" \
                   f"app_id=7913379&" \
                   f"v=1.58.6&" \
                   f"redirect_uri=https://vk.com/feed&" \
                   f"uuid={self._generate_uuid()}&" \
                   f"scheme=space_gray&" \
                   f"action={base64.b64encode(json.dumps(action).encode('ascii')).decode('UTF-8')}&" \
                   f"initial_stats_info={base64.b64encode(json.dumps(initial_stats_info).encode('ascii')).decode('UTF-8')}"

        # Дозвон до вкида, ради реализма, и чтобы вытянуть анонимку из html
        resp = self.session.get(vkid_url)
        self.access_token = RE_PARSE_ANON.findall(resp.text)[0]

        validate_url = "https://api.vk.com/method/auth.validateAccount?v=5.207&client_id=7913379"
        params = {
            "login": login,
            "sid": "",
            "client_id": 7913379,
            "auth_token": self.access_token,
            "super_app_token": "",
            "supported_ways": "push, email",
            "passkey_supported": "",
            "access_token": ""
        }

        resp_existing = self.session.post(validate_url, params=params)

        try:
            login_data = VKIDResponseHandle(resp_existing.json()).data

            if 'is_phone' in login_data and login_data['is_phone']:
                self.login_type = self.LoginType.phone.value
            else:
                self.login_type = self.LoginType.email.value

            if 'flow_name' in login_data:
                self.flow_name = login_data['flow_name']

                if self.flow_name == self.FlowName.need_registration:
                    raise AuthException(AuthException.REG_NEEDED, {
                        'login': login,
                        'login_type': self.login_type
                    })
            if 'sid' in login_data:
                self.sid = login_data['sid']
        except VKIDException as e:
            if e.code == VKIDException.CAPTCHA_NEEDED:
                raise AuthException(AuthException.CAPTCHA_NEEDED, e.data)
            raise

        # {'error':
        # {'error_code': 104, 'error_msg': 'Not found: Login not found'
        # {'error_code': 14, 'error_msg': 'Captcha needed', captcha_sid': '600515107069', 'captcha_img': 'https://api.vk.com/captcha.php?sid=600515107069&resized=1', 'captcha_ts': 1682805118.313, 'captcha_attempt': 1, 'captcha_height': 80, 'captcha_width': 208
        # {'error_code': 1000, 'error_subcode': 1111, 'error_msg': 'Invalid phone number: phone has invalid format'
        # {'response': {'is_phone': True, 'flow_name': 'need_password_and_validation', 'sid': 'loginvalidate_6fb792fcebb7dae62b881e704542d3a3'}}
        # {'response': {'is_phone': True, 'flow_name': 'need_registration'}}
        # {'response': {'is_email': True, 'flow_name': 'need_password_and_validation', 'sid': 'loginvalidate_b01013ee38f947f6601fd35bd389e465'}}

        # {"error":{"error_code":1000,"error_subcode":1111,"error_msg":"Invalid phone number: phone is incorrect"

    def _auth_page_password(self, password):

        pass_uri = "https://login.vk.com/?act=connect_authorize"
        self.device_id = self._generate_uuid()
        payload = {
                     "user": {
                         "first_name": "",
                         "last_name": ""
                     }
                 }

        redirect_to = base64.b64encode(
            ('https://vk.com/feed?payload=' +
                 urllib.parse.quote(
                     json.dumps(
                        payload, separators=(",",":")
                    )
                 )
             ).encode('ascii')
        ).decode('UTF-8')
        params = {
            "username": self.login,
            "password": password,
            "auth_token": self.access_token,
            "sid": "",
            "uuid": self._generate_uuid(),
            "v": "5.207",
            "device_id": self.device_id,
            "service_group": "",
            "expire": "",
            "save_user": 1,
            "to": redirect_to,
            "version": 1,
            "app_id": 7913379
        }
        resp = self.session.post(pass_uri, params=params, headers={
            "origin": "https://id.vk.com",
            "referer": "https://id.vk.com/",
        })
        try:
            print(resp.content)
            data = LegacyResponseHandle(resp.json()).data
            print(data)
            self.access_token = data['access_token']
            self.next_step_url = data['next_step_url']
            resp2 = self.session.post(self.next_step_url)
            if "vk.com/feed" in resp2.url:
                return VKUserPC(self.session.cookies, self.device_id, self.session.headers['User-Agent'],
                                self.access_token)
            else:
                raise AuthException(AuthException.LEGACY_BAD_REQUEST, resp2.json())
        except AuthException:
            raise

    def auth(self) -> VKUserPC:
        self._parse_params()
        self._auth_page_login(self.login)
        return self._auth_page_password(self.password)
