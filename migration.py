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

    def __init__(self, user: VKUserPC):
        self.user = user

    # def by_link(self):
    #     user_auth = LinkAuth().
    #     try:
    #         u_token = user_auth.get_token()
    #         if 'error' in u_token:
    #             if u_token['error_code'] == 4:
    #                 raise MigrationError(MigrationError.EXPIRED, data=u_token)
    #         else:
    #             u_token = u_token['access_token']
    #             print(u_token)
    #     except Exception:
    #         raise

    def migrate(self):
        linkauth = LinkAuth()
        link = linkauth.get_auth_link()
        print(link)

        self.user.session.get(link)
        code_re = re.compile(r'\?q=(\w*)')
        code = code_re.findall(link)[0]

        legacy_resp = self.user.session.post('https://login.vk.com/?act=connect_internal', params={
            "app_id": self.__app_id_pc,
            "version": 1,
            "access_token": user.access_token
        }, headers={
            "origin": "https://id.vk.com",
            "referer": "https://id.vk.com/"
        })

        token = legacy_resp.json()['data']['access_token']


        params = json.dumps({
            "auth_code":code, "action":"0"
        })
        params = {
            "code": f'return [API.auth.processAuthCode({params})];',
            "access_token": token,
            "client_id": self.__app_id_android,
            "v": "5.204"
        }
        self.user.session.get(link)
        self.user.session.post("https://api.vk.com/method/execute", params=params)

        params = json.dumps({
            "auth_code": code, "action": "1"
        })
        params = {
            "code": f'return [API.auth.processAuthCode({params})];',
            "access_token": token,
            "client_id": self.__app_id_android,
            "v": "5.204"
        }
        self.user.session.get(link)
        self.user.session.post("https://api.vk.com/method/execute", params=params)

        resp = linkauth.get_token()

        print(resp)
        token = resp['access_token']

        return VKUserMobile(token=token, device_id=linkauth.device_id, UA=linkauth.UA)

    def get_feed(self):
        print(
            self.user.session.get("https://vk.com/feed").text
        )

# mig = Migration(login=login, password=password)
# mig.myhttp()
#



if __name__ == "__main__":

    login = 'saida.ku4irova@yandex.ru'
    password = 'mustik2012'

    user = vkid_auth.VKIDAuth(login, password).auth()

    # with open('users/1.usr', 'rb') as us:
    #     user = VKUserPC.loads(us.read())

    usermob = Migration(user).migrate()
    print(usermob.token)
    print(usermob.UA)
    print(usermob.device_id)

    usermob.api.http.proxies = {"http": "bigbate02_gmail_com:f4566456ed@86.62.18.35:30009",
                                "https": "bigbate02_gmail_com:f4566456ed@86.62.18.35:30009"}


    print('Обновляем сломанный токен')
    refreshed_params = usermob.refresh_broken_token(password)
    [print(key, refreshed_params[key]) for key in refreshed_params.keys()]

    print('/\n')
    print('/\n')

    print('Обновляем полученный обновленный сломанный токен с рецептом')
    vodka_token = vodka.refresh_token(refreshed_params['access_token'])

    print(vodka_token)

    usermob.token = vodka_token
    usermob.api.token['access_token'] = vodka_token

    print(usermob.api.token)

    print('/\n')
    print('/\n')

    print('Получаем эксченж из починенного рецептом токена')
    exchange_token = usermob.get_exchange_token()
    print(exchange_token)

    print('/\n')
    print('/\n')

    print('Пытаемся обновить токены валидными методами ВК')
    refresh_result = usermob.refresh_tokens(exchange_token)
    print(refresh_result)
    usermob.api.token['access_key'] = refresh_result['success'][0]['access_token']['token']
    usermob.token = refresh_result['success'][0]['access_token']['token']

    print('/\n')
    print('/\n')

    print('Получаем фулл валидный мобильный эксченж')
    mobile_exchange = usermob.get_exchange_token()

    print('Мобильный эксченж: ', mobile_exchange)
    [print(f'{key}:', refresh_result['success'][0][key]) for key in refresh_result['success'][0].keys()]















