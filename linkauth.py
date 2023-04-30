import asyncio
import random
import re
import string
import time

import requests

def generate_random_string(length, characters):
    return ''.join(random.choice(characters) for _ in range(length))


def get_random_vkuuid():
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits + '_' + '-', k=24))


def get_device_id():
    return generate_random_string(21, "0123456789abcdef")

def random_ua():
    vk_versions = [
        "8.11-15060",
        "8.25-15920",
        "8.24-15831",
        "8.21-15632"
    ]
    android_versions = [
        "Android 11; SDK 30",
        "Android 12; SDK 31",
        "Android 10; SDK 29",
        "Android 9; SDK 28"
    ]
    proc_version = ["arm64-v8a"]
    phone_model = ["Redmi Note 7",
                   "Google Pixel 4a",
                   "Samsung Galaxy Note 20",
                   "OnePlus 9 Pro",
                   "Xiaomi Mi 11",
                   "OPPO Reno6 5G",
                   "Vivo V20",
                   "Redmi Note 11 Pro",
                   "Redmi A2"]
    lang = ["ru"]
    extension = ["1920x1080"]
    return f"VKAndroidApp/{random.choice(vk_versions)} ({random.choice(android_versions)}; {random.choice(proc_version)}; " \
           f"{random.choice(phone_model)}; {random.choice(lang)}; {random.choice(extension)})"


class LinkAuth:
    def __init__(self, UA=None, device_id=None):
        self._session = requests.Session()
        self.UA = random_ua() if not UA else UA
        self._session.headers['User-Agent'] = self.UA
        self.device_id = get_device_id() if not device_id else device_id
        self.token = self.get_anonym_token()
        self._auth_code = None
        self._auth_hash = None
        self._auth_id = None
        self._expires_in = None
        self._on_parse_event = asyncio.Event()

    def device_name(self):
        return re.findall("\((.*?)\)", self.UA)[0]

    def get_anonym_token(self):
        with self._session.post('https://api.vk.com/oauth/get_anonym_token/', params={
            'client_id': 2274003,
            'client_secret': 'hHbZxrka2uZ6jB1inYsH',
            'lang': 'ru',
            'https': 1,
            'device_id': self.device_id,
            'v': '5.209',
            'app_id': 2274003
        }) as resp:
            data = resp.json()
            if 'token' in data:
                return data['token']
            raise Exception("Anonymous token not received")

    def get_auth_link(self):
        ses = requests.Session()
        ses.headers['User-Agent'] = self.UA
        ses.headers['origin'] = 'https://id.vk.com'
        ses.headers['referer'] = 'https://id.vk.com/'
        ses.headers['sec-ch-ua-platform'] = "Android"
        ses.headers['sec-ch-ua-mobile'] = "?1"
        ses.headers['sec-ch-ua'] = self.device_name()

        resp = ses.post('https://api.vk.com/method/auth.getAuthCode',
                        params={
                            'v': "5.207",
                            'client_id': "2274003",
                            'device_name': self.device_name(),
                            'auth_code_flow': "",
                            'verification_hash': "",
                            'force_regenerate': 'true',
                            'anonymous_token': self.token,
                            'access_token': ""
                        }
                    )
        data = resp.json()
        if data['response']:
            self._auth_code = data['response']['auth_code']
            self._auth_hash = data['response']['auth_hash']
            self._auth_id = data['response']['auth_id']
            self._expires_in = data['response']['expires_in']
            return data['response']['auth_url']
        raise Exception("Auth Url not received")

    def get_token(self):
        with requests.session() as ses:
            ses.headers['User-Agent'] = self.UA
            ses.headers['origin'] = 'https://id.vk.com'
            ses.headers['referer'] = 'https://id.vk.com/'
            ses.headers['sec-ch-ua-platform'] = "Android"
            ses.headers['sec-ch-ua-mobile'] = "?1"
            ses.headers['sec-ch-ua'] = self.device_name()
            while True:
                #   print('checkAuthCode')
                with ses.post('https://api.vk.com/method/auth.checkAuthCode', params={
                    'v': "5.207",
                    'client_id': "2274003",
                    'auth_hash': self._auth_hash,
                    'anonymous_token': self.token
                }) as resp:
                    data = resp.json()

                    if 'error' in data:
                        raise Exception(data)

                    if data['response']['status'] == 4:
                        return {'error': 'expired', 'error_code': 4}

                    if data['response']['status'] == 2:
                        return data['response']

                    time.sleep(3)
