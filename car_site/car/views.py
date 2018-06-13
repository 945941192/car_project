
#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

import os,stat,socket,traceback
import subprocess,threading
import time,datetime
import base64
import json
import re
import time
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
            "photo_time":"12345678","plate_number":"冀J0R6A3","photo_paht":"/var/ftp/pub/luo/20180607/冀J0R6A3",        # CarPhoto
            "total_weight":"100kg","speed":"80","temperature":"90",                                                     # HeartData
            "savedb_time":"1992202020",                                                                                 # AxisData
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
    if request.method == "GET":
        car_obj = [{
                "photo_time":"12345678","plate_number":"冀J0R6A3","photo_path":"/var/ftp/pub/luo/20180607/冀J0R6A3",
                "total_weight":"100kg","speed":"80","temperature":"90",
                "savedb_time":"1992202020",
        }]
        return render(request,"car/car_constantly.html",{"car_obj":car_obj})

    elif request.method == "POST":
        car_obj = [{
                "photo_time":"12345678",
		        "plate_number":"冀J0R6A3",
	    	    "photo_path":"<img src=\"/static/test/冀J0R6A3\"  style=\"text-align:center;width: 100px;\" alt=\"system_process-img\" class=\"img-rounded\">",
                "savedb_time":"1992202020",
                "total_weight1":"100kg",
                "total_weight2":"100kg",
                }]
                    
        from car.models import Axisdata,Carphoto,Heartdata
        CarPhoto_set = Carphoto.objects.all().order_by("-id")[:5]
        Axisdata_set = Axisdata.objects.all()
        list1 = []
        for obj in CarPhoto_set:
            print "*"*10,obj.id, "*"*10,obj.carno
            car_line ={
                    "photo_time":None,
		            "plate_number":None,
	    	        "photo_path":None,
                    "savedb_time":None,
                    "total_weight1":None,
                    "total_weight2":None
                    }
            try:
                car_newest_ticks = Axisdata.objects.filter(carno = obj.carno).order_by('-id')[0].ticks
            except Exception as e:
                time_local = time.localtime(obj.ticks)
                car_line["photo_time"] = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
                car_line["plate_number"] = obj.carno
                car_line["photo_path"] ="<img src=\"{pathname}\"  style=\"text-align:center;width: 100px;\" alt=\"system_process-img\" class=\"img-rounded\">".format(pathname=obj.pathname.replace("/var","/static")),
                car_line["savedb_time"] = "数据处理中"
                car_line["total_weight1"] = 100
                car_line["total_weight2"] = 100
                list1.append(car_line)
                print e
                continue

            car_info_set =  Axisdata.objects.filter(ticks = car_newest_ticks)
            time_local = time.localtime(obj.ticks)
            car_line["photo_time"] = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
            print "time = ",time.strftime("%Y-%m-%d %H:%M:%S",time_local)
            car_line["plate_number"] = obj.carno
            #car_line["photo_path"] = obj.pathname
            car_line["photo_path"] ="<img src=\"{pathname}\"  style=\"text-align:center;width: 100px;\" alt=\"system_process-img\" class=\"img-rounded\">".format(pathname=obj.pathname.replace("/var","/static")),
            time_save = time.localtime(car_newest_ticks)
            car_line["savedb_time"] = time.strftime("%Y-%m-%d %H:%M:%S",time_save)
            car_line["total_weight1"] = 100
            car_line["total_weight2"] = 100
            list1.append(car_line)

    
        data ={
                "draw":5,
                "recordsTotal":5,
                "recordsFiltered":5,
                "data":list1
                }
        return JsonResponse(data)
 
