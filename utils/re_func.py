import re


def tel_match(tel):
    """
    手机号正则验证
    :param tel:
    :return:
    """
    if re.match(r"^1[35678]\d{9}$", tel):
        return True
    else:
        return False