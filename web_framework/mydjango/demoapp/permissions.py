# -*- coding: utf-8 -*-

from rest_framework import permissions

from django.contrib.auth.models import User

"""
增加了自定义的权限类
http://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/
"""
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        #print type(obj) , obj.username, request.user
        #TODO 如何判断 Obj Class 分类


        """
        这句判断的让 aa 成为了 超级用户
        注意: aa 如果未设置 is_staff 有效用户, 可以登录后台, 这里的判断也不会发生作用
        """
        #print "debug: permissions.py obj owner = %s, login username = %s" % (obj.username, request.user.username )
        if request.user.username == 'aa':
            return True

        #如果别的类用的字段不叫owner, 在这里要用 if 判断一下
        if str(type(obj)) == '<class \'django.contrib.auth.models.User\'>':
            #
            #用户名判断
            #print obj.username == request.user.username
            #用户判断
            return obj == request.user
        else:
            return obj.owner == request.user
