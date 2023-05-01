import json
import re
import time

import requests
from bs4 import BeautifulSoup
import vk_api
import datetime
from classes import VKUserPC, VKUserMobile
from vkid_auth import VKIDAuth
from linkauth import LinkAuth
login = "saida.ku4irova@yandex.ru"
password = "mustik2012"
login2 = "t.levkina@list.ru"
password2 = "Tania179"
import bs4

class MigrationError(Exception):
    EXPIRED = "Session Expired"
    def __init__(self, error, data = None):
        self.message = error
        super().__init__(self.message)

        self.data = data




class Migration:
    def __init__(self, user: VKUserPC):
        self.user = user


    def migrate2(self):
        linkauth = LinkAuth()
        link = linkauth.get_auth_link()
        print(link)

        self.user.session.get(link)
        code_re = re.compile(r'\?q=(\w*)')
        code = code_re.findall(link)[0]
        #https://oauth.vk.com/authorize?client_id=6121396&scope=1073737727&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1
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

    def migrate(self):
        resp = self.user.session.get(
            "https://oauth.vk.com/authorize?client_id=6121396&scope=1073737727&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1"
        )
        soup = BeautifulSoup(resp.text, "html.parser")
        script = soup.find_all('script')[1]
        next_step_url = re.search(r'location\.href = "([\w:\/.?=&%]*)"\+', script.text).groups()[0]
        resp = self.user.session.get(next_step_url)
        return resp.url.split("%253D")[1].split("%2526")[0]

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
    #token = Migration(user).migrate()

    ses = requests.Session()

    with open("code.txt", 'r') as f:
        code = f.read()
        print(ses.post("https://api.vk.com/method/execute", params={
            "code":code,
            'access_token': token,
            'v':'5.201'}).json())











