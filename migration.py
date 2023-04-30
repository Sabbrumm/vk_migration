import json
import re
import time

import vk_api
import datetime
from classes import VKUserPC, VKUserMobile
from vkid_auth import VKIDAuth
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
        #
        # legacy_resp = self.user.session.post('https://login.vk.com/?act=connect_internal', params={
        #     "app_id":7913379,
        #     "version":1,
        #     "access_token":""
        # }, headers={
        #     "origin": "https://id.vk.com",
        #     "referer": "https://id.vk.com/"
        # })
        #
        # token = legacy_resp.json()['data']['access_token']
        #
        #
        # params = json.dumps({
        #     "auth_code":code, "action":"0"
        # })
        # params = {
        #     "code": f'return [API.auth.processAuthCode({params})];',
        #     "access_token": token
        # }
        # self.user.session.get(link)
        # self.user.session.post("https://api.vk.com/method/execute?v=5.204&client_id=7913379", params=params)
        #
        # params = json.dumps({
        #     "auth_code": code, "action": "1"
        # })
        # params = {
        #     "code": f'return [API.auth.processAuthCode({params})];',
        #     "access_token": token
        # }
        # self.user.session.get(link)
        # self.user.session.post("https://api.vk.com/method/execute?v=5.204&client_id=7913379", params=params)
        #
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
    with open('users/1.usr', 'rb') as us:
        user = VKUserPC.loads(us.read())

    usermob = Migration(user).migrate()
    print(usermob.token)
    print(usermob.UA)
    print(usermob.device_id)
    usermob.method_info()











