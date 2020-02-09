#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.exceptions import APIException


class ParamError(APIException):
    status_code = 400
    default_detail = '参数有误'

    def __init__(self, err):
        self.detail = err

    def __str__(self):
        return self.detail


class APIQueryError(APIException):
    """第三方接口错误类"""
    status_code = 400
    default_detail = '查询有误!!'

    def __init__(self, err):
        self.detail = err

    def __str__(self):
        return self.detail
