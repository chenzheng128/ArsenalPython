# -*- coding: utf-8 -*-
from django.db import models

"""
#创建一个person类，定义两个字段 姓名，年龄
"""


class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()

    """
    #定义toString，便于输出调试
    # 在Python3中使用 def __str__(self)
    """

    def __unicode__(self):
        return ("%s (%d)") % (self.name, self.age)


# Create your models here.

"""
#创建一个Article类，定义4个字段
"""


class Article(models.Model):
    title = models.CharField(u'标题', max_length=256)
    content = models.TextField(u'内容')

    pub_date = models.DateTimeField(u'发表时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)


    # 自定义简要标题，仅显示前50个字符
    def contentShortFunc(self):
        if len(self.content) > 50:
            return self.content[:50]
        else:
            return self.content

    contentShortFunc.short_description = "标题（简要）"

    contentShort = property(contentShortFunc)


"""
#创建一个Student类，定义两个字段 姓名，年龄

owner = models.ForeignKey(Student)
"""


class Student(models.Model):
    name = models.CharField(u'姓名', max_length=30)
    grade = models.IntegerField(u'年级')

    def __unicode__(self):
        return ("%s (%d)") % (self.name, self.grade)


# class Book(models.Model):
#     owner = models.ForeignKey(Student)
#     name = models.CharField(u'书名', max_length=30)
#     grade = models.IntegerField(u'年级')
#     pub_date = models.DateTimeField(u'出版时间')