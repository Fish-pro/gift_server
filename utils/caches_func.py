import logging

from django.core.cache import caches

from gift_server.config import TOKEN_TIMEOUT


def save_token(token, user):
    """
    缓存tokne
    :param token:
    :param user:
    :return:
    """
    user_info = {
       "uuid": user.uuid,
       "userObj": user,
    }
    try:
        caches["client"].set(token, user_info, TOKEN_TIMEOUT)
    except Exception as e:
        logging.error(str(e))
        return False
    check_token = caches["client"].get(user.uuid)
    if check_token:
        try:
            caches["client"].delete(check_token)
        except Exception as e:
            logging.error(str(e))
            return False
    try:
        caches["client"].set(user.uuid, token, TOKEN_TIMEOUT)
    except Exception as e:
        logging.error(str(e))
        return False
    return True


