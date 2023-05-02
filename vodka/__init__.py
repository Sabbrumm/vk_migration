from vodka.DefaultUserTalk import DefaultUserTalk
from vodka.TokenReceiver import TokenReceiver


def get_token(login, password, auth_code=None, serialized_proxy=None, user_talk=DefaultUserTalk()):
    """пример функции default user talk смотрите в библе"""
    receiver = TokenReceiver(login, password, auth_code, serialized_proxy, user_talk=user_talk)
    return receiver.get_token()


def refresh_token(token):
    receiver = TokenReceiver()
    receipt = receiver._get_receipt()
    refreshed_token = receiver._refresh_token(token, receipt)
    return refreshed_token
