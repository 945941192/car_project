
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
import os

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
    json_name = "channel_conf.json"
    conf_dir = os.path.dirname(os.path.abspath(__file__)) + "/" + json_name
    data = json.loads(subprocess.check_output("cat %s"%(conf_dir),shell=True))
    channel1_n = data.get("channel1")
    channel2_n = data.get("channel2")
    channel3_n = data.get("channel3")
    channel4_n = data.get("channel4")
    data = {}
    zhou_name_list = list(set(["zhou%s"%_.axisno for _ in obj_list]))
    zhou_dict = dict()
    print zhou_name_list  

    for zhou in zhou_name_list:
        zhou_weight = list()
        for _ in obj_list:
            if (_.channel == 1 or _.channel ==2) and _.axisno == int(zhou.replace("zhou","")):
                N = eval("channel%s_n"%_.channel)
                zhou_weight.append(round(_.sum/N, 2))
        zhou_dict[zhou] = sum(zhou_weight)
    zhou_dict["weight1"] = sum([ val for key,val in zhou_dict.items() ])

    return zhou_dict

def weight2(obj_list):
    """
        param:channel:编号为1,2传感器,在同一时间下承受的质量和为  weight1
        由 轴1 轴2  至  可能到10个轴的 重量和
        {"zhou1":50,"zhou2":30,"weight2":70}
    """
    json_name = "channel_conf.json"
    conf_dir = os.path.dirname(os.path.abspath(__file__)) + "/" + json_name
    data = json.loads(subprocess.check_output("cat %s"%(conf_dir),shell=True))
    channel1_n = data.get("channel1")
    channel2_n = data.get("channel2")
    channel3_n = data.get("channel3")
    channel4_n = data.get("channel4")
    data = {}
    zhou_name_list = list(set(["zhou%s"%_.axisno for _ in obj_list]))
    zhou_dict = dict()
    print zhou_name_list  

    for zhou in zhou_name_list:
        zhou_weight = list()
        for _ in obj_list:
            if (_.channel == 3 or _.channel ==4) and _.axisno == int(zhou.replace("zhou","")):
                N = eval("channel%s_n"%_.channel)
                zhou_weight.append(_.sum/N)
        zhou_dict[zhou] = sum(zhou_weight)
    zhou_dict["weight2"] = sum([ val for key,val in zhou_dict.items() ])

    return zhou_dict

def get_html_code(weight_info, tag=None, num=None):
    print "weight_info",weight_info
    th_html = "".join([ r'''<th  style="text-align:center;">轴%s</th>'''%(i.replace("zhou",''))  for i in weight_info if "weight" not in i ])
    td_html = "".join([ r'''<td>%d</td>'''%y  for i,y in weight_info.items() if "weight" not in i ])
    print "td_htlm====", td_html

    html_table = r'''
                    <table class="table" id="test2">
                      <thead>
                        <tr>
                        %s
                        </tr>
                      </thead>
                      <tbody>
                                <tr>
                                    %s
                                </tr>
                      </tbody>
                    </table>'''%(th_html, td_html)

    html_code = r'''
<button class="btn btn-round btn-info" data-toggle="modal" data-target=%s>%s</button>
<div class="modal fade" id=%s tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title" id="myModalLabel">
                    轴重
                </h4>
            </div>
            <div class="modal-body">
            %s
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭
                </button>
            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
</div>'''%("#"+str(num)+str(tag),weight_info["weight%s"%tag],str(num)+str(tag),html_table)
    return html_code

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
            CarPhoto_set = Carphoto.objects.all().order_by("-id")[:5]
            list1 = []
            for obj in CarPhoto_set:
                car_line ={
                        "photo_time":None,
                        "plate_number":None,
                        "photo_path":None,
                        }

                time_local = time.localtime(obj.ticks)
                car_line["photo_time"] = time.strftime("%H:%M:%S",time_local)
                car_line["plate_number"] = obj.carno
                car_line["photo_path"] ="<img src=\"{pathname}\"  style=\"text-align:center;width: 100px;\" alt=\"system_process-img\" class=\"img-rounded\">".format(pathname=obj.pathname.replace("/var","/static")),
                list1.append(car_line)

        
            data ={
                    "draw":5,
                    "recordsTotal":5,
                    "recordsFiltered":5,
                    "data":list1
                    }
            return JsonResponse(data)
 
        elif tag == "b":
            # 获取AxisData 最新五辆车的数据
            list1 = []
            list1 = list()
        
            from car.models import Axisdata
            new_car_time = list(set([ obj.ticks for obj in  Axisdata.objects.all().order_by("-id")[:100] ]))
            new_car_time.sort(reverse=True)
            print new_car_time
            for i in  new_car_time[:5]:
                car_line = {
                    "save_time":None,
                    "weight1":None,
                    "weight2":None,
                    }
                obj_list = Axisdata.objects.filter(ticks=i)
                weight_info = {"weight1_info":weight1(obj_list),"weight2_info":weight2(obj_list)}
                print i,weight_info
                car_line["save_time"] = time.strftime("%H:%M:%S",time.localtime(i))
                #car_line["weight1"] = weight_info["weight1_info"]["weight1"]
                #car_line["weight2"] = weight_info["weight2_info"]["weight2"]
                car_line["weight1"] = get_html_code(weight_info["weight1_info"], tag="1", num=i)
                car_line["weight2"] = get_html_code(weight_info["weight2_info"], tag="2", num=i)
                list1.append(car_line)
          
            
            data ={
                    "draw":5,
                    "recordsTotal":5,
                    "recordsFiltered":5,
                    "data":list1
                    }
            return JsonResponse(data)

@csrf_exempt
def handle_channel_conf(request):

    import subprocess
    import json
    if request.method == "GET":
        channel = request.GET.get("channel1")
        json_name = "channel_conf.json"
        conf_dir = os.path.dirname(os.path.abspath(__file__)) + "/" + json_name
        if not channel:
            
            data = json.loads(subprocess.check_output("cat %s"%(conf_dir),shell=True))
            return render(request,"car/channel_config.html",data)
        else:
            channel1 = float(request.GET.get("channel1"))
            channel2 = float(request.GET.get("channel2"))
            channel3 = float(request.GET.get("channel3"))
            channel4 = float(request.GET.get("channel4"))
            channel_conf_json = {"channel1":channel1,"channel2":channel2,"channel3":channel3,"channel4":channel4}
            open(conf_dir,"w").write(json.dumps(channel_conf_json))
            return HttpResponseRedirect(reverse("car:channel_conf"))

