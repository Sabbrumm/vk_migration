import time

import requests
import pickle

import vk_api
from requests.cookies import RequestsCookieJar

class VKUserPC:
    def __init__(self, cookies:RequestsCookieJar, device_id:str, UA:str):
        self.cookies = cookies
        self.session = requests.session()
        self.session.cookies = cookies
        self.device_id = device_id
        self.UA = UA
        self.session.headers['User-Agent'] = UA

    def dumps(self):
        return pickle.dumps(self)

    @classmethod
    def loads(cls, pickle_data:bytes):
        object_:VKUserPC = pickle.loads(pickle_data)
        return object_

class VKUserMobile:
    def __init__(self, token:str, device_id:str, UA:str):
        self.token = token
        self.device_id = device_id
        self.UA = UA

    def dumps(self):
        return pickle.dumps(self)

    @classmethod
    def loads(cls, pickle_data:bytes):
        object_:VKUserPC = pickle.loads(pickle_data)
        return object_

    def method_info(self):
        us = vk_api.VkApi(token=self.token)
        us.http.headers["User-Agent"] = self.UA
        user_info = us.method('users.get', {})
        user_info = us.method('execute.getUserInfo', {
            "androidManufacturer": "Google",
            "wide": "0",
            "device_id": self.device_id,
            "visible_time": int(time.time() * 1000),
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
            "v": "5.210",
            "lang": "ru",
            "https": 1,
        })

        print(user_info)


if __name__ == "__main__":
    us = VKUserMobile(
        "vk1.a.QxGPUpvdrJeVvA54dz3XXCSObhf3tJHwPo6aeiStdAUNwsGphI7r0tqfoonxPNDowcv87ptwRrGAGmlwgWCdcW9nhn-DUtB_c5fTZ7cXD1Yppdbas5oLWFCAKZdM-eRQ3mfZgEmpyzP-d5bg-9ueKqrrPr-MgVP79ZdSOy2newi7_TQeHOLVrocsN_iLMjqa",
        "VKAndroidApp/8.11-15060 (Android 9; SDK 28; arm64-v8a; Redmi Note 11 Pro; ru; 1920x1080)",
        "5e555f65a9a1b305"
    )
    us.method_info()