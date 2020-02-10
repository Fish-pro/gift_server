#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import path

from manager.views import LoginViews, UserListGenericMixinAPIView, InitManagerViews

app_name = 'manager'

urlpatterns = [
    path('init/', InitManagerViews.as_view()),  # 初始化管理员
    path('login/', LoginViews.as_view()),  # 登录
    path('user/', UserListGenericMixinAPIView),  # 用户

]