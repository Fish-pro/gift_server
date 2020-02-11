import logging

from manager.models import LoginLog


def save_login_log(request, user):
    """
    保存登陆日志
    :param user:
    :return:
    """
    try:
        LoginLog.objects.create(
            ipAddr=request.META.get('HTTP_X_FORWARDED_FOR', None),
            userUuid=user.uuid,
            userAgent=request.META.get('HTTP_USER_AGENT', ''),
            isManager=user.isManager
        )
    except Exception as e:
        logging.error(str(e))
        return False
    return True