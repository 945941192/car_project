
#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

import os,stat,paramiko,socket,traceback
import subprocess,threading
import time,datetime
import base64
import json
import re
from car.models import Axisdata,Carphoto,Heartdata

@csrf_exempt
def handle_index(request):
    #return render(request,"index/index.html")
    return HttpResponseRedirect(reverse("car:car_constantly"))

@csrf_exempt
def handle_car_constantly(request):
    """
        实时数据展示
        {
            "photo_time":"12345678","plate_number":"冀J0R6A3","photo_paht":"/var/ftp/pub/luo/20180607/冀J0R6A3",
            "total_weight":"100kg","speed":"80","temperature":"90",
            "savedb_time":"1992202020",
            "car_axle1":"80kg",
            "car_axle2":"80kg",
            "car_axle3":"80kg",
            "car_axle4":"80kg",
            "car_axle5":"80kg",
            "car_axle6":"80kg",
            "car_axle7":"80kg",
            "car_axle8":"80kg",
            "car_axle9":"80kg",
            "car_axle10":"80kg",
        }
    """
    car_obj = [{
                "photo_time":"12345678","plate_number":"冀J0R6A3","photo_path":"/var/ftp/pub/luo/20180607/冀J0R6A3",
                "total_weight":"100kg","speed":"80","temperature":"90",
                "savedb_time":"1992202020",
                "car_axle1":"80kg",
                "car_axle2":"80kg",
                "car_axle3":"80kg",
                "car_axle4":"80kg",
                "car_axle5":"80kg",
                "car_axle6":"80kg",
                "car_axle7":"80kg",
                "car_axle8":"80kg",
                "car_axle9":"80kg",
                "car_axle10":"80kg",
        }]
    return render(request,"car/car_constantly.html",{"car_obj":car_obj})
