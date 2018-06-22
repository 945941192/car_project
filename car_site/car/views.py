
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


def weight1(obj_list):
    """
        param:channel:编号为1,2传感器,在同一时间下承受的质量和为  weight1
        由 轴1 轴2  至  可能到10个轴的 重量和
        {"zhou1":50,"zhou2":30,"weight1":70}
    """
    channel1_n = 1
    channel2_n = 1
    channel3_n = 3
    channel4_n = 4
    data = {}
    zhou_name_list = list(set(["zhou%s"%_.axisno for _ in obj_list]))
    zhou_dict = dict()
    print zhou_name_list  

    for zhou in zhou_name_list:
        zhou_weight = list()
        for _ in obj_list:
            if (_.channel == 1 or _.channel ==2) and _.axisno == int(zhou.replace("zhou","")):
                N = eval("channel%s_n"%_.channel)
                zhou_weight.append(_.sum/N)
        zhou_dict[zhou] = sum(zhou_weight)
    zhou_dict["weight1"] = sum([ val for key,val in zhou_dict.items() ])

    return zhou_dict


@csrf_exempt
def handle_car_constantly(request):
    """
        实时数据展示
        {
            "photo_time":"08:30:30",
            "plate_number":"冀J0R6A3",
            "photo_paht":"/var/ftp/pub/luo/20180607/冀J0R6A3",        # CarPhoto
        }
    """
    tag = request.GET.get("tag")
    print "*",tag
    from car.models import Axisdata,Carphoto,Heartdata
    obj_list = Axisdata.objects.filter(carno = "鲁NUY093").filter(ticks="1528375405")
    weight1(obj_list)
    
    if request.method == "GET":
        return render(request,"car/car_constantly.html")

    elif request.method == "POST":
        if tag == "a":            
            print "*"*100
            CarPhoto_set = Carphoto.objects.all().order_by("-id")[:5]
            list1 = []
            print "2"
            for obj in CarPhoto_set:
                print "2.1"
                car_line ={
                        "photo_time":None,
                        "plate_number":None,
                        "photo_path":None,
                        }
                print "2.2"

                time_local = time.localtime(obj.ticks)
                print "2.3"
                car_line["photo_time"] = time.strftime("%H:%M:%S",time_local)
                car_line["plate_number"] = obj.carno
                car_line["photo_path"] ="<img src=\"{pathname}\"  style=\"text-align:center;width: 100px;\" alt=\"system_process-img\" class=\"img-rounded\">".format(pathname=obj.pathname.replace("/var","/static")),
                list1.append(car_line)

            print "3"
        
            data ={
                    "draw":5,
                    "recordsTotal":5,
                    "recordsFiltered":5,
                    "data":list1
                    }
            print data
            print "()"*100
            return JsonResponse(data)
 
        elif tag == "b":
            # 获取AxisData 最新五辆车的数据
        
            from car.models import Axisdata
            new_car_time = list(set([ obj.ticks for obj in  Axisdata.objects.all().order_by("-id")[:100] ]))
            list2 = list()
            for i in  new_car_time:
                obj_list = Axisdata.objects.filter(ticks=i)
                list2.append(weight1(obj_list))
            
            print list2
            pass
            return "hello"
