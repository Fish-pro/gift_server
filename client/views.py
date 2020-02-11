from django.contrib.auth.hashers import check_password
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from client.client_filter import save_login_log
from client.serializers import UserSerializer, WorkSerializer, UserWorkSerializer
from manager.models import UserAuth, User, Work, UserWork
from utils.auths import CustomAuthentication
from utils.caches_func import save_token
from utils.paginations import MyPagination
from utils.random_func import get_token
from utils.re_func import tel_match
from utils.return_func import http_return

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

class LoginViews(APIView):
    '''登录视图'''
    authentication_classes = None

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
        if not save_login_log(req, checkTel.userUuid):
            return http_return(400, "存储登录日志失败")
        return http_return(200, "登录成功", return_token(token, checkTel.userUuid))
    
class WorkViews(APIView):
    '''事务视图'''
    authentication_classes = CustomAuthentication

    def get(self, req):
        user = User.objects.filter(uuid=req.user.get("uuid")).first()
        works = Work.objects.filter(userUuid=user, status=1).all()
        return Response(WorkSerializer(works).data)

class UserWorkViews(APIView):
    '''用户送礼视图'''
    authentication_classes = CustomAuthentication

    def get(self, req):
        uuid = req.query_params.get("uuid", None)
        sortType =  req.query_params.get("sortType", None)
        if not uuid:
            return http_return(400, "请选择要查看宾客的事务")
        work = Work.objects.filter(uuid=uuid, status=1).first()
        if not work:
            return http_return(400, "事务不存在")
        userWork = UserWork.objects.filter(workUuid=work, status=1)
        if sortType == "createTime":
            userWorks = userWork.order_by("-createTime").all()
        elif sortType == "money":
            userWorks = userWork.order_by("-money").all()
        elif sortType == "name":
            userWorks = userWork.order_by("userUuid__name").all()
        else:
            return http_return(400, "请选择排序方式")
        pg = MyPagination()
        pager_user_works = pg.paginate_queryset(queryset=userWorks, request=req, view=self)
        ser = UserWorkSerializer(instance=pager_user_works, many=True)
        return pg.get_paginated_response(ser.data)

class SearchViews(APIView):
    '''搜索视图'''
    authentication_classes = CustomAuthentication

    def get(self, req):
        uuid = req.query_params.get("uuid", None)
        if not uuid:
            return http_return(400, "请选择要搜索的事务")
        work = Work.objects.filter(uuid=uuid, status=1).first()
        if not work:
            return http_return(400, "事务不存在")
        keyword = req.query_params.get("keyword", None)
        if not keyword:
            return http_return(400, "请输入搜索关键词")
        res_queryset = UserWork.objects.filter(workUuid=work, userUuid__name__icontains=keyword, status=1).order_by("-money").all()
        return Response(UserWorkSerializer(res_queryset, many=True).data)