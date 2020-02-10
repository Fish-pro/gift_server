from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from client.client_filter import save_login_log
from manager.filters import UsersFilter
from manager.models import UserAuth, User
from manager.serializers import UserSerializer
from utils.caches_func import save_token
from utils.errors import ParamError
from utils.random_func import get_token
from utils.re_func import tel_match
from utils.return_func import http_return
from utils.return_info import USER_NOT_EXIST


def return_token(token,user):
    """
    返回登录token和用户信息
    :param token:
    :param user:
    :return:
    """
    data = {
        "token": token,
        "profile": UserSerializer(user, many=False).data,
    }
    return data
class InitManagerViews(APIView):
    '''初始化管理员'''
    authentication_classes = []
    permission_classes = []

    @transaction.atomic  # 加事务锁
    def post(self,req):
        manager = User.objects.filter(status=1,isManager=True).first()
        if not manager:
            user = User.objects.create(
                name="管理员",
                address="镇雄县",
                gender=1,
                age=20,
                isManager=True,
            )
            UserAuth.objects.create(
                userUuid=user,
                tel="18487241833",
                password=make_password("123456")
            )
        return http_return(200, "初始管理员化成功")


class LoginViews(APIView):
    '''登录视图'''
    authentication_classes = []
    permission_classes = []

    def post(self, req):
        tel = req.data.get("tel", None)
        if not tel:
            return http_return(400, "请输入登录手机号")
        if not tel_match(tel):
            return http_return(400, "请输入正确的手机号")
        password = req.data.get("password", None)
        if not password:
            return http_return(400, "请输入登录密码")
        checkTel = UserAuth.objects.filter(tel=tel).first()
        if not checkTel:
            return http_return(400, "手机号未记录")
        if not check_password(password, checkTel.password):
            return http_return(400, "登录密码不正确")
        token = get_token()
        if not save_token(token, checkTel.userUuid):
            return http_return(400, "服务器缓存错误")
        if not save_login_log(req):
            return http_return(400, "存储登录日志失败")
        return http_return(200, "登录成功", return_token(token, checkTel.userUuid))


class UserListGenericMixinAPIView(GenericAPIView,
                                  ListModelMixin,
                                  CreateModelMixin,
                                  RetrieveModelMixin,
                                  UpdateModelMixin,
                                  DestroyModelMixin):
    queryset = User.objects.filter(status=1).all()
    serializer_class = UserSerializer
    filter_class = UsersFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering = ("name",)

    @transaction.atomic  # 加事务锁
    def create(self, request, *args, **kwargs):
        pass

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            raise ParamError(USER_NOT_EXIST)
        serializer = UserSerializer(instance)
        return Response(serializer.data)

    @transaction.atomic  # 加事务锁
    def update(self, request, *args, **kwargs):
        pass

    @transaction.atomic  # 加事务锁
    def destroy(self, request, *args, **kwargs):
        pass





