#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import path

from .views import LoginViews, WorkViews, UserWorkViews, SearchViews

app_name = 'client'

urlpatterns = [
    path('login/', LoginViews.as_view()), # 登录
    path('works/', WorkViews.as_view()), # 事务列表视图
    path('userWorks/', UserWorkViews.as_view()), # 事务用户列表视图
    path('search/', SearchViews.as_view()), # 搜索视图

]