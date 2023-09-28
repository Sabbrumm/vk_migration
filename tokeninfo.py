import requests
from linkauth import get_random_vkuuid, random_ua
from linkauth import LinkAuth

UA = "SAK_1.107(com.vk.admin)/1.4-227 (Android 11; SDK 30; armeabi-v7a; Google sdk_gphone_x86; en; 2280x1080)"#random_ua()
target = 2274003
app_id = 6121396
device_id = get_random_vkuuid()
v = "5.209"
token = "vk1.a.hdwKTn__cpilfa7k90-NJ0YJWsRlC96BLofQpkypL3DZYwHX4pGdxybBJLerYzBBe7Qq4xV3ymcsmXSi7gd5Urvk-1InKOGB43NC0CVs9_Bfy6c8hSFAgjz4Pw51M4MqkBKSSO1A8toyH8ZaAa0fzFD_pd5qLDSncMBrtPLqOVueF5tDZdtUG5YVsLj-t9C--6AecItiFxo86HeMEZcuEA"
tkn = "vk1.a.CUZaMO3wu_3LPIublcn2ljHAVPSTOb77fMQWPsAoFu7Y_LLFn_GBVUfxhJ3b2scRT2x3vMUewvWcTgDAAaWwNSbIW1D9nqbPfOL1eA1YSAvyRwoTK0S-H113euwYLqzOkbt5PHZH5IMn0saHHO_5Zs9tQru4X0dHadTlvEDeoPaPy1l5Olbi5X_lKO5rE7SY"

exc_token = "vk1.a.Wy8Wwtw00eGso9kNHvXEmQpUKxezt6Sh-FvlE0Hmvzp7lo986DV0akAw9I6Vgo9683u4D1gjLpStWrPedBSB7iQhYyLdOR-_LJxC9gM9689iEwfX5OP7_aFHlnjY_Bg75RhSmNvnoYRGl3jdDjCHwusQf_l2D0syx-phQ4y6KChA2nB2Fyog9jKa7U7VniQP"






method = "auth.getTokenInfo"

ses = requests.session()
ses.headers['User-Agent'] = UA




with ses.post('https://api.vk.com/oauth/get_anonym_token/', params={
    'client_id': 6121396,
    'client_secret': 'L3yBidmMBtFRKO9hPCgF',
    'lang': 'ru',
    'https': 1,
    'device_id': device_id,
    'v': '5.209',
    'app_id': 6121396
}) as resp:
    data = resp.json()
    if 'token' in data:
        acc_t = data['token']



resp = ses.post(f"https://api.vk.com/method/{method}", params={
    "target_app_id":target,
    "access_token": tkn,
    "exchange_token": acc_t,
    "lang":"en",
    "v":v,
    "https":1,
    "api_id":target
})

print(resp.status_code)
try:
    print(resp.json())
except:
    print("No json")


 # вебверсия с сикретом
#6287487
#QbYic1K3lEV5kTGiqlq2