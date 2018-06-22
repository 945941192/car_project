#!/usr/bin/env python
# coding=utf-8

from django.conf.urls import url

from . import views

urlpatterns = [
    # index
    url(r'^$',views.handle_index,name='index'),
    # 汽车实时数据
    url(r'^constantly$',views.handle_car_constantly,name='car_constantly'),
    # 传感器参数设置
    url(r'^channel_con$',views.handle_channel_conf,name='channel_conf'),
]
