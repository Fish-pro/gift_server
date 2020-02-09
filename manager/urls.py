#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import path

from manager.views import LoginViews, UserListGenericMixinAPIView

app_name = 'manager'

urlpatterns = [
    path('login/', LoginViews.as_view()),  # 登录
    path('user/', UserListGenericMixinAPIView),  # 用户

]