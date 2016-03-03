# -*- coding: utf-8 -*-

"""cuczhongchou URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin


"""
rest url define START >>>

http://www.django-rest-framework.org/tutorial/quickstart/


TESTING:
curl -H 'Accept: application/json; indent=4' -u admin:amin http://127.0.0.1:8000/users/
"""
from django.contrib.auth.models import User
from rest_framework import routers
from  demoapp import views

router = routers.DefaultRouter()
# 注册 users 与 groups view 使用默认的router 后台管理
# router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'articles', views.ArticleViewSet)
router.register(r'reporters', views.ReporterViewSet)

# 注册 Post Rest 接口
# router.register(r'Post', views.PostViewSet)

# router.register(r'snippets22', views.SnippetList, base_name="Snippet")

"""
rest url define END <<<
"""

urlpatterns = [

    #REST LOGIN
    url(r'^rest\/api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # #REST  snippets
    # #test cmd # http http://127.0.0.1:8000/d01/rest_snippets/3/
    # # snippet_list2 是使用 @api_view() 优化过的版本
    url(r'^rest\/snippets/$', views.snippet_list),
    url(r'^rest\/snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),

    url(r'^rest\/snippets2/$', views.snippet_list2),
    url(r'^rest\/snippets2/(?P<pk>[0-9]+)/$', views.snippet_detail2),


    #tutorial3 http://www.django-rest-framework.org/tutorial/3-class-based-views/
    #snippet 继承单个ApiView类
    url(r'^rest\/snippets3/$', views.SnippetList.as_view()),
    url(r'^rest\/snippets3/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),

    #snippet 使用 多个模板类 简化
    url(r'^rest\/snippets3B/$', views.SnippetListB.as_view()),
    url(r'^rest\/snippets3B/(?P<pk>[0-9]+)/$', views.SnippetDetailB.as_view()),

    #snippet 最简化版本
    url(r'^rest\/snippets3C/$', views.SnippetListC.as_view()),
    url(r'^rest\/snippets3C/(?P<pk>[0-9]+)/$', views.SnippetDetailC.as_view()),

    #tutorial4 http://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/
    # 列举用户, 及其包含的 snippets

    url(r'^rest\/snippets4/$', views.SnippetListD.as_view()),
    url(r'^rest\/snippets4/(?P<pk>[0-9]+)/$', views.SnippetDetailD.as_view()),

    url(r'^rest\/users4/$', views.UserListD.as_view()),
    url(r'^rest\/users4/(?P<pk>[0-9]+)/$', views.UserDetailD.as_view()),


    # tutorial5 http://www.django-rest-framework.org/tutorial/5-relationships-and-hyperlinked-apis/
    url(r'^rest5\/', views.api_root5),

    url(r'^rest\/snippets5/$',
        views.SnippetList5.as_view(), name='snippet-list5'),
    #TODO -detail -list 是一个约束好的名字, 用snippet-detail5 会导致错误
    url(r'^rest\/snippets5/(?P<pk>[0-9]+)/$',
        views.SnippetDetail5.as_view(), name='snippet-detail'),
    url(r'^rest\/snippets5/(?P<pk>[0-9]+)/highlight/$',
        views.SnippetHighlight5.as_view(), name='snippet-highlight5'),
    url(r'^rest\/users5/$',
        views.UserList5.as_view(), name='user-list5'),
    url(r'^rest\/users5/(?P<pk>[0-9]+)/$',
        views.UserDetail5.as_view(), name='user-detail'),

    ### demoapp 官方 overview https://docs.djangoproject.com/en/1.8/intro/overview/
    # 使用 include 和 namespace file:///Users/chen/coding/documentations/django-docs-1.8-en/intro/tutorial03.html
    url(r'^d01/', include('demoapp.urls', namespace="polls")) ,

    ### learn 自强学社的参考代码
    url(r'^learn/', include('learn.urls')),
    #
    url(r'^admin/', include(admin.site.urls)),

]

#print urlpatterns
"""
打开这个配置, 可以在符合api_view的函数类中, 追加 .json .api 访问接口

http://www.django-rest-framework.org/tutorial/2-requests-and-responses/
"""
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = format_suffix_patterns(urlpatterns)

#router.urls 和 format_suffix_patterns 冲突了, 下移
# #rest-framework  http://www.django-rest-framework.org/#requirements
urlpatterns += [
    url(r'^rest\/', include(router.urls)) ,
]




#print urlpatterns