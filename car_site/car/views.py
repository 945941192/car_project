
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
from car import *

@csrf_exempt
def handle_car_real_time(request):
    return render(request,"index/index.html")
