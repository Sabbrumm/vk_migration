import enum
import json
import re

import vkid_auth
import vodka
from classes import VKUserPC, VKUserMobile
from linkauth import LinkAuth

login = "saida.ku4irova@yandex.ru"
password = "mustik2012"
login2 = "t.levkina@list.ru"
password2 = "Tania179"


class MigrationError(Exception):
    EXPIRED = "Session Expired"

    def __init__(self, error, data = None):
        self.message = error
        super().__init__(self.message)

        self.data = data


class Migration:
    __app_id_pc = 7913379
    __app_id_android = 2274003
    class MigrateType(enum.Enum):
        QR_REFRESH = 'qr_refresh'
        QR_SWAPTYPE = 'qr_swaptype'
        VKADMIN = 'VKADMIN'

    def __init__(self, user: VKUserPC):
        self.user = user
        self.proxies = None


    def use_proxies(self, proxies:dict):
        """Конструкторный метод. Прям при инициализации просто ебошим"""
        self.proxies = proxies
        self.user.set_proxies(proxies)
        return self

    def __accept_log_in_qr(self, link):
        code_re = re.compile(r'\?q=(\w*)')
        code = code_re.findall(link)[0]

        # Прогружаем страничку

        self.user.session.get(link)


        # Отдаем запрос на получение временного токена на страничке

        legacy_resp = self.user.session.post('https://login.vk.com/?act=connect_internal',
                                             params={
                                                 "app_id": self.__app_id_pc,
                                                 "version": 1,
                                                 "access_token": user.access_token
                                             },
                                             headers={
                                                 "origin": "https://id.vk.com",
                                                 "referer": "https://id.vk.com/"
                                             })

        token = legacy_resp.json()['data']['access_token']


        # Прогружаем инфу о логине

        params = json.dumps({
            "auth_code": code, "action": "0"
        })
        params = {
            "code": f'return [API.auth.processAuthCode({params})];',
            "access_token": token,
            "client_id": self.__app_id_android,
            "v": "5.204"
        }
        self.user.session.post("https://api.vk.com/method/execute",
                               params=params)


        # Даём добро

        params = json.dumps({
            "auth_code": code, "action": "1"
        })
        params = {
            "code": f'return [API.auth.processAuthCode({params})];',
            "access_token": token,
            "client_id": self.__app_id_android,
            "v": "5.204"
        }
        self.user.session.post("https://api.vk.com/method/execute",
                               params=params)

    def migrate_qr_refresh(self, password:str = None):
        """Позволяет мигрировать через цепочку получение -> Exchange-обновление с паролем -> Receipt-обновление -> Exchange-обновление"""

        linkauth = LinkAuth()

        link = linkauth.get_auth_link()
        self.__accept_log_in_qr(link)

        resp = linkauth.get_token()
        token = resp['access_token']
        user_mob = VKUserMobile(token=token, device_id=linkauth.device_id, UA=linkauth.UA)

        if self.proxies:
            user_mob.set_proxies(self.proxies)

        print('Обновляем с Exchange-password')
        exc_pass_params = user_mob.exchange_password_refresh(password)

        print('Обновляем с Receipt')
        receipt_token = vodka.refresh_token(exc_pass_params['access_token'])
        user_mob.set_new_token(receipt_token)

        print('Обновляем с Exchange-free')
        refresh_result = user_mob.exchange_free_refresh()
        access_token = refresh_result['success'][0]['access_token']['token']
        user_mob.set_new_token(access_token)

        return user_mob

# mig = Migration(login=login, password=password)
# mig.myhttp()
#



if __name__ == "__main__":

    login = 'saida.ku4irova@yandex.ru'
    password = 'mustik2012'

    user = vkid_auth.VKIDAuth(login, password).auth()

    # with open('users/1.usr', 'rb') as us:
    #     user = VKUserPC.loads(us.read())

    usermob = Migration(user).use_proxies(
        {"http": "bigbate02_gmail_com:f4566456ed@86.62.18.35:30009",
         "https": "bigbate02_gmail_com:f4566456ed@86.62.18.35:30009"}
    ).migrate_qr_refresh(password)

    print(usermob.get_user_info())
