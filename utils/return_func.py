import json

from django.http import HttpResponse


def http_return(code, msg='', info=None):
    """
    返回封装
    :param code: 状态码
    :param msg: 返回消息
    :param info: 返回数据
    :return:
    """
    data = {
        'code': code,
        'msg': msg
    }
    if info is not None:
        data['data'] = info
    return HttpResponse(json.dumps(data), status=code)
