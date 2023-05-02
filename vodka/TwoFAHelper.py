import requests

from vodka.CommonParams import CommonParams
from vodka.TokenException import TokenException


class TwoFAHelper:
    def __init__(self):
        self._params = CommonParams()

    def validate_phone(self, validation_sid, serialized_proxies: dict):
        session = requests.session()
        session.proxies = serialized_proxies
        self._params.set_common_vk(session)
        dec = session.get("https://api.vk.com/method/auth.validatePhone", params=[
            ('sid', validation_sid),
            ('v', '5.131')
        ]).json()
        if 'error' in dec or 'response' not in dec:
            raise TokenException(TokenException.TWOFA_ERR, dec)
