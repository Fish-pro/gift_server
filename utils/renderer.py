#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.renderers import JSONRenderer


class MyJsonRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        try:
            code = data['code']
            msg = data['msg']
            renderer_context['response'].status_code = 400 if data.get('code')>600 else data.get('code')
            res = {
                'code': code,
                'msg': msg
            }
        except:
            # 表示程序是正常运行的，需自己组装code和msg参数
            code = 200
            msg = 'OK'
            renderer_context['response'].status_code = 200
            res = {
                'code': code,
                'msg': msg,
                'data': data,
            }
        # print(res)
        return super().render(res, accepted_media_type, renderer_context)
