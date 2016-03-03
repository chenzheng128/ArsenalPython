# -*- coding: utf-8 -*-
from django.conf.urls import url
import views

"""
定义url便于 include
"""

urlpatterns = [

    url(r'^questions2$', views.index2, name='index2'),

    # ex: /polls/5/
    # 手工实现view
    #url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    #url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),


    # file:///Users/chen/coding/documentations/django-docs-1.8-en/intro/tutorial04.html#amend-urlconf
    url(r'^quest/$', views.IndexView.as_view(), name='index'),
    url(r'^quest/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^quest/(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^quest/(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),



    url(r'^articles/([0-9]{4})/$', views.year_archive),
    # url(r'^articles/([0-9]{4})/([0-9]{2})/$', views.month_archive),
    # url(r'^articles/([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.article_detail),
    url(r'^snoop/$', views.snoop),

]
