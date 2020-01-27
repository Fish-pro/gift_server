import logging

from django.core.cache import caches
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission


class CustomAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN')
        if not token:
            raise AuthenticationFailed('提供有效的身份认证标识')
        try:
            user_info = caches['default'].get(token)
        except Exception as e:
            logging.error(str(e))
            raise AuthenticationFailed('连接Redis失败')
        if not user_info:
            raise AuthenticationFailed('请登录后重新访问')
        return user_info, token