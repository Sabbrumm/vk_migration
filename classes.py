import time
import requests
import pickle
from requests.cookies import RequestsCookieJar
from vk_api import VkApi, ApiHttpError, ApiError, CAPTCHA_ERROR_CODE, Captcha


class VkApiMob(VkApi):
    def method(self, method, values=None, captcha_sid=None, captcha_key=None,
               raw=False):
        """ Вызов метода API

        :param method: название метода
        :type method: str

        :param values: параметры
        :type values: dict

        :param captcha_sid: id капчи
        :type captcha_key: int or str

        :param captcha_key: ответ капчи
        :type captcha_key: str

        :param raw: при False возвращает `response['response']`
                    при True возвращает `response`
                    (может понадобиться для метода execute для получения
                    execute_errors)
        :type raw: bool
        """

        values = values.copy() if values else {}

        if 'v' not in values:
            values['v'] = self.api_version

        if 'https' not in values:
            values['https'] = 1

        if 'lang' not in values:
            values['lang'] = 'en'

        if self.token:
            values['access_token'] = self.token['access_token']

        if captcha_sid and captcha_key:
            values['captcha_sid'] = captcha_sid
            values['captcha_key'] = captcha_key

        with self.lock:
            # Ограничение 3 запроса в секунду
            delay = self.RPS_DELAY - (time.time() - self.last_request)

            if delay > 0:
                time.sleep(delay)

            response = self.http.post(
                'https://api.vk.com/method/' + method,
                values,
                headers={'Cookie': ''}
            )
            self.last_request = time.time()

        if response.ok:
            response = response.json()
        else:
            error = ApiHttpError(self, method, values, raw, response)
            response = self.http_handler(error)

            if response is not None:
                return response

            raise error

        if 'error' in response:
            error = ApiError(self, method, values, raw, response['error'])

            if error.code in self.error_handlers:
                if error.code == CAPTCHA_ERROR_CODE:
                    error = Captcha(
                        self,
                        error.error['captcha_sid'],
                        self.method,
                        (method,),
                        {'values': values, 'raw': raw},
                        error.error['captcha_img']
                    )

                response = self.error_handlers[error.code](error)

                if response is not None:
                    return response

            raise error

        return response if raw else response['response']


class VKUserPC:
    def __init__(self, cookies:RequestsCookieJar, device_id:str, UA:str, access_token):
        self.cookies = cookies
        self.session = requests.session()
        self.session.cookies = cookies
        self.device_id = device_id
        self.UA = UA
        self.session.headers['User-Agent'] = UA
        self.access_token = access_token

    def set_proxies(self, proxies:dict):
        self.session.proxies = proxies
    def dumps(self):
        return pickle.dumps(self)

    @classmethod
    def loads(cls, pickle_data:bytes):
        object_:VKUserPC = pickle.loads(pickle_data)
        return object_


class VKUserMobile:
    __v = "5.210"
    __app_id = 2274003

    def __init__(self, token: str, device_id: str, UA: str):
        self.token = token
        self.device_id = device_id
        self.UA = UA
        self.api = VkApiMob(token=self.token, api_version=self.__v)
        self.api.http.headers["User-Agent"] = self.UA
        self.api.http.headers["x-vk-android-client"] = "new"

    def set_proxies(self, proxies:dict):
        self.api.http.proxies = proxies

    def set_new_token(self, access_token:str):
        self.token = access_token
        self.api.token['access_token'] = access_token

    def dumps(self):
        return pickle.dumps(self)

    @classmethod
    def loads(cls, pickle_data:bytes):
        object_:VKUserMobile = pickle.loads(pickle_data)
        return object_

    def get_user_info(self):
        user_info = self.api.method('execute.getUserInfo', {
            "androidManufacturer": "Google",
            "wide": "0",
            "device_id": self.device_id,
            "visible_time": int(time.time()),
            "func_v": "30",
            "info_fields": "audio_ads,"
                           "audio_background_limit,"
                           "country,"
                           "discover_design_version,"
                           "discover_preload,"
                           "discover_preload_not_seen,gif_autoplay,"
                           "https_required,inline_comments,"
                           "intro,"
                           "lang,"
                           "menu_intro,"
                           "money_clubs_p2p,"
                           "money_p2p,"
                           "money_p2p_params,"
                           "music_intro,"
                           "audio_restrictions,"
                           "profiler_settings,"
                           "raise_to_record_enabled,"
                           "stories,"
                           "masks,"
                           "subscriptions,"
                           "support_url,"
                           "video_autoplay,"
                           "video_player,"
                           "vklive_app,"
                           "community_comments,"
                           "webview_authorization,"
                           "story_replies,"
                           "animated_stickers,"
                           "live_section,"
                           "podcasts_section,"
                           "playlists_download,"
                           "calls,"
                           "security_issue,"
                           "eu_user,"
                           "wallet,"
                           "vkui_community_create,"
                           "vkui_profile_edit,"
                           "vkui_community_manage,"
                           "vk_apps,"
                           "stories_photo_duration,"
                           "stories_reposts,"
                           "live_streaming,"
                           "live_masks,"
                           "camera_pingpong,"
                           "role,"
                           "video_discover,"
                           "vk_identity,"
                           "clickable_stickers,"
                           "phone_verify,"
                           "bugs,"
                           "show_vk_apps_intro,"
                           "link_redirects,"
                           "qr_promotion,"
                           "valid_from,"
                           "send_common_network_stats_until,"
                           "send_images_network_stats_until,"
                           "comment_restriction,"
                           "shopping_params,"
                           "is_topic_expert,"
                           "cache,"
                           "page_size,"
                           "newsfeed,"
                           "vk_pay_endpoint,"
                           "invite_link,"
                           "market_orders,"
                           "js_injections,"
                           "menu_ads_easy_promote,"
                           "phone,"
                           "subscription_combo_allowed,"
                           "stories,"
                           "im_user_name_type,"
                           "show_only_not_muted_messages,"
                           "messages_recommendation_list_hidden,"
                           "side_menu_custom_items,"
                           "obscene_text_filter,"
                           "market_adult_18plus",
            "supported_navigation_features": "sa_redesign_v3, "
                                             "sa_redesign_v3_p2,"
                                             "sa_redesign_v3_profile",
            "androidVersion": "33",
            "needExchangeToken": "1",
            "fields": "exports,"
                      "country,"
                      "sex,"
                      "status,"
                      "bdate,"
                      "first_name_gen,"
                      "last_name_gen,"
                      "verified,"
                      "trending,"
                      "domain,"
                      "followers_count,"
                      "image_status,"
                      "bdate_visibility,"
                      "is_nft",
            "androidModel": "SM-A226B",
            "v": "5.185"                       # Важно, токен сломанный, версия выше 5.185 не заведётся, 5.210 не юзать!
        })
        return user_info

    def get_exchange_token(self):
        return self.get_user_info()["exchange_token"]

    def _non_legacy_token_refresh(self, exchange_token, password):
        '''
        Обычные обновления эксченжа через этот метод делать НЕЛЬЗЯ из-за возможных блокировок!
        Для обычных обновлений токена юзается новый метод auth.refreshTokens
        Этот метод использовался в приложении как авторизация эксченжа при выходе из аккаунта, не для его обновления
        '''
        params: dict = {
            "exchange_token": exchange_token,
            "v": self.__v,
            "api_id": self.__app_id,
            "client_id": self.__app_id,
            "device_id": self.device_id,
            "scope": "all",                                             # offline не ставить, ловишь bad client
            "sak_version": "1.108",
            "password": password                                        # пиздец
        }
        oauth_blank = self.api.http.post(
            "https://api.vk.com/oauth/auth_by_exchange_token",
            params,
            allow_redirects=True
        )
        k_vs = oauth_blank.url.removeprefix('https://oauth.vk.com/blank.html#').split('&')
        response_params: dict = {k_v.split('=')[0]: k_v.split('=')[1] for k_v in k_vs}
        return response_params

    def exchange_password_refresh(self, password, exchange_token=None) -> dict:
        exchange_token = exchange_token if exchange_token else self.get_exchange_token()
        refreshed_params = self._non_legacy_token_refresh(exchange_token, password)
        return refreshed_params

    def exchange_free_refresh(self, exchange_token=None):
        exchange_token = exchange_token if exchange_token else self.get_exchange_token()
        '''
            Валидное токенов по эксченжу
        '''
        method_name = "auth.refreshTokens"
        params = {
            "exchange_tokens": exchange_token,
            "device_id": self.device_id,
            "scope": "all",
            "initiator": "expired_token",
            "active_index": "0",
            "client_secret": "hHbZxrka2uZ6jB1inYsH",
            "lang": "en",
            "client_id": self.__app_id,
            "api_id": self.__app_id,
            "v": self.__v,
            "https": 1
        }
        response = self.api.http.post(f"https://api.vk.com/method/{method_name}", params)
        return response.json()['response']