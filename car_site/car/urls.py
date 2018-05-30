#!/usr/bin/env python
# coding=utf-8

from django.conf.urls import url

from . import views

urlpatterns = [
    # index
    url(r'^$',views.handle_index,name='index'),
    # 汽车实时数据
    url(r'^test$',views.handle_car_real_time,name='car_real_time'),
]
