# -*- coding: utf-8 -*-
from django.conf.urls import url
import views

"""
定义url便于 include
"""

urlpatterns = [
    # url(r'^$', views.index, name='index'),

    # ex: /polls/5/
    # 手工实现view
    #url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    #url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),


    ### learn 自强学社

 	# step02 Examples: 增加learn 应用中的 views.py 模块 中的 simple(request) 方法
    url(r'^step02/$', 'learn.views.step02', name='step02'),# Notice this line

    # step03 Examples: 从/add/?a=4&b=5 读取参数
    url(r'^step03a/$', 'learn.views.add', name='add'), # 注意修改了这一行

    # 采用 /add/3/4/ 这样的网址的方式
    url(r'^step03b/(\d+)/(\d+)/$', 'learn.views.add2', name='add2'),

    # step04 Examples: 增加learn 应用中的 views.py 模块 中的 index(request) 方法
    url(r'^step04a/$', 'learn.views.step04a', name='learnStep04a'),# Notice this line

    url(r'^step04b/$', 'learn.views.step04b', name='learnStep04b'),# Notice this line

    url(r'^step05/$', 'learn.views.step05', name='learnStep05'),# Notice this line

    url(r'^step06a/$', 'learn.views.step06a', name=''),# Notice this line

    url(r'^step06b/$', 'learn.views.step06b', name=''),

    url(r'^step06c/$', 'learn.views.step06c', name=''),

    url(r'^step06d/$', 'learn.views.step06d', name=''),

    url(r'^step07/$', 'learn.views.step07', name=''),

    url(r'^step09/$', 'learn.views.step09', name=''),


]
