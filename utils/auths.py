import logging

from django.contrib.auth.models import AnonymousUser
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


class ClientAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN')
        if not token:
            raise AuthenticationFailed('提供有效的身份认证标识')
        try:
            user_info = caches['client'].get(token)
        except Exception as e:
            logging.error(str(e))
            raise AuthenticationFailed('连接Redis失败')
        if not user_info:
            raise AuthenticationFailed('请登录后重新访问')
        return user_info, token


class CustomAuthorization(BasePermission):

    message = '对不起，你没有权限'

    def has_permission(self, request, view):
        # 当前用户的权限缓存
        if not request.user or isinstance(request.user, AnonymousUser):
            return True
        # path = request.path
        # if not path.startswith("/api/manage/"):
        #     return False
        # for role in request.user.roles.all():
        #     for permission in role.permissions.all():
        #         if permission.url in request.path:
        #             return True
        # return False
        return True
