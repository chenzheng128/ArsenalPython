# -*- coding: utf-8 -*-
import time
import json

from django.shortcuts import render
from django.core.urlresolvers import reverse

# Create your views here.
from django.http import HttpResponse

# 常见异常import
from exceptions import ValueError
from django.template import loader, Template, Context
from django.utils.datastructures import MultiValueDictKeyError


# step02 默认首页
from learn.models import Person

# step09 引入我们创建的表单类
from .forms import AddForm


def step02(request):
    return HttpResponse(u'''欢迎光临 传媒众筹网!
    	<br>
    	<a href="./add/?a=4&b=5">add 处理参数方式1</a> 
    	<br>
    	<a href="./add/3/4/">add2 处理参数方式2</a> 

    	''')


# step03 处理add;
# step03 Examples: 从/add/?a=4&b=5 读取参数
# urls.py url(r'^add/$', 'learn.views.add', name='add'),
def add(request):
    try:
        a = request.GET['a']
        b = request.GET['b']
        c = int(a) + int(b)
        return HttpResponse("从/add/?a=4&b=5 读取参数:" + "a+b= " + str(c))

    # 参数异常处理
    except ValueError as e:
        return HttpResponse("参数类型错误： 请输入数值" + str(e))
    except MultiValueDictKeyError as e:
        return HttpResponse("缺少参数: " + str(e))
    except Exception as e:
        print type(e)
        return HttpResponse("异常错误：" + str(e))


# 采用 /add/3/4/ 这样的网址的方式
# urls.pyurl(r'^add/(\d+)/(\d+)/$', 'learn.views.add2', name='add2'),
def add2(request, a, b):
    c = int(a) + int(b)
    thisUrl = reverse('add2', args=(a, b));
    return HttpResponse(
        u"""
    	<br>/add/3/4/ 网址的方式 读取参数: a+b= %d
    	<br> %s       网址的方式 读取参数: a+b= %d ; (网址由 reverse('add2', args=(a,b)) 函数生成)

    	""" % (c, thisUrl, c))


def step04a(request):
    # return HttpResponse("默认空页面");
    return render(request, 'home.html')


def step04b(request):
    # return HttpResponse("默认空页面");
    return render(request, 'base_extend.html')


"""
step05 列出数据库现有person对象
"""


def step05(request):
    template = loader.get_template('person_list.html')
    html = template.render(Context({'person_list': Person.objects.all()}))
    return HttpResponse(html)


"""
* /step06a/ 在模板 step06a.html 中显示变量信息
"""

 
def step06a(request):
    timeStr = time.strftime('%Y-%m-%d %H:%M:%S')
    someVar = u"当前时间为" + timeStr
    return render(request, 'step06a.html', {'myVar': someVar})


"""
* /step06b/ 显示List列表(for语法）信息在模板(step06b.html)中
"""


def step06b(request):
    TutorialList = ["HTML", "CSS", "jQuery", "Python", "Django"]
    return render(request, 'step06b.html', {'TutorialList': TutorialList})

"""
* /step06c/ 显示Dict字典(for语法）信息在模板(step06c.html)中
"""

def step06c(request):
    info_dict = {'site': u'自强学堂', 'content': u'各种IT技术教程'}
    return render(request, 'step06c.html', {'info_dict': info_dict})


"""
* /step06d/ 条件判断显示(if 语法）    在模板(step06d.html)中
"""

def step06d(request):
    List = map(str, range(100))# 一个长度为100的 List
    info_dict={}
    for x in range(10):              # 一个长度为10的 Dict              
        info_dict['key'+str(x)]=x 
    return render(request, 'step06d.html', {'List': List, 'info_dict': info_dict})


"""
* /step07/ python对象(List,Dict)转换为json在模板中加载
"""

def step07(request):
    List = ['list1', 'list2', 3, 5, 7]
    Dict = {'site': 'nic.cuc.edu.cn', 'author': 'zhchen', 'country':'中国'}
    return render(request, 'step07.html', {
            'List': json.dumps(List),
            'Dict': json.dumps(Dict)
        })

"""
* /step09/ 使用 Django 的 表单 (forms)
"""

def step09(request):
    if request.method == 'POST':# 当提交表单时
     
        form = AddForm(request.POST) # form 包含提交的数据
         
        if form.is_valid():# 如果提交的数据合法
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            return HttpResponse(str(int(a) + int(b)))
     
    else:# 当正常访问时
        form = AddForm()
    return render(request, 'step09.html', {'form': form})
