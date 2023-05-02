from vodka.VkClient import VkClient

KATE = VkClient(
    u'KateMobileAndroid/56 lite-460 (Android 4.4.2; SDK 19; x86; unknown Android SDK built for x86; en)',
    u'lxhD8OD7dMsqtXIm5IUY',
    u'2685278'
)

_VK_UA = u'VKAndroidApp/6.54-9332 (Android 11; SDK 30; armeabi-v7a; YoYo; en; 2400x1080)'
VK_UA = u'VKAndroidApp/8.15.1-15289 (Android 11; SDK 30; armeabi-v7a; Anubis; ru; 2960x1440)'

VK_OFFICIAL = VkClient(
    VK_UA,
    u'hHbZxrka2uZ6jB1inYsH',
    u'2274003'
)
