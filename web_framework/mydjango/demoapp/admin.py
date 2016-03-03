# -*- coding: utf-8 -*-
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import *

# Register your models here.

def create_modeladmin(model, modeladmin, name = None, verbose_name = None):
    """
    创建模型的不同管理视图  http://stackoverflow.com/questions/2223375/multiple-modeladmins-views-for-same-model-in-django-admin
    :param modeladmin:
    :param model:
    :param name:
    :return:
    """
    class  Meta:
        proxy = True
        app_label = model._meta.app_label
        verbose_name_plural = verbose_name

    attrs = {'__module__': '', 'Meta': Meta}

    newmodel = type(name, (model,), attrs)

    admin.site.register(newmodel, modeladmin)
    return modeladmin


"""
rest Tutorial snippets
"""
admin.site.register(Snippet)

"""
d02 admin
"""
admin.site.register(D02Album)
admin.site.register(D02Musician)

admin.site.register(D02Person)
admin.site.register(D02Group)
admin.site.register(D02Membership)

"""
d01 admin overview
"""

# Overview
admin.site.register(D01Article)
admin.site.register(D01Reporter)


"""
# d01 admin 投票管理
# Tutorial polls
# admin.site.register(Question);
# admin.site.register(Choice);
"""


class ChoiceInline(admin.TabularInline):  # 比 StackedInline 更精简的模式
    # class ChoiceInline(admin.StackedInline):   from

    model = Choice
    extra = 2  # 每次新增的数量


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date',
                    'was_published_recently', 'checked')  # 在列表中显示栏目
    list_filter = ['pub_date', 'checked']  # 筛选
    search_fields = ['question_text']  # 文本搜索

    fieldsets = [  # 定义表单组合, 不出现在这的字段,不会出现在表单中
        (None, {'fields': ['question_text', 'checked']}),

        ('填写组合', {'fields': ['pub_date', 'author'], 'classes': ['collapse']}),  # collapse 增加折叠效果
    ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)

"""
#博客管理
"""

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'checked', 'publish_date', 'user', 'status', )  # 列表显示的字段
    search_fields = ('title',)  # 列表包含根据指定字段搜索
    list_filter = ('publish_date',)  # 右侧过滤选项

    # 分组表单
    fieldsets = (
        ('基本信息', {'fields': ('title', 'checked', 'content', 'excerpt', 'publish_date', 'status', 'user', 'categories', 'tags')}),
        ('Meta Data', {'fields': ('alias', 'keywords', 'description', )}),
    )

class PostQuickAdmin(ImportExportModelAdmin):
    list_display = ('title', 'checked', 'publish_date', 'user', 'status', )  # 列表显示的字段
    pass


class PostAdminCheck(admin.ModelAdmin):
    list_display = ('title', 'checked',)  # 列表显示的字段
    search_fields = ('title',)  # 列表包含根据指定字段搜索
    list_filter = ('publish_date',)  # 右侧过滤选项

    # 分组表单
    fieldsets = (
        ('基本信息', {'fields': ('title', 'checked', 'content', 'excerpt', 'publish_date', 'status', 'user', 'categories', 'tags')}),
        ('Meta Data', {'fields': ('alias', 'keywords', 'description', )}),
    )


from django.utils.safestring import mark_safe
from django.contrib import messages
def add_format_message(request, level, msg):
    """
     增加带 color 颜色的 msg 提醒
    """
    color=""
    if level == messages.INFO:      color="blue"
    elif level == messages.WARNING: color="yellow"
    elif level == messages.ERROR:   color="red"
    elif level == messages.DEBUG:   color="gray"
    else: color="black"

    msg = "<font color=%s>%s</font>" % (color, msg)
    messages.add_message(request, messages.INFO, mark_safe(msg))
class PostCustomMessageAdmin(admin.ModelAdmin):
    """
    自定义保存消息ModelAdmin
    参考message framework: https://docs.djangoproject.com/en/dev/ref/contrib/messages/
    """
    list_display = ('title', 'checked', 'publish_date', 'user', 'status', )  # 列表显示的字段
    fieldsets = (
        ('基本信息', {'fields': ('title', 'checked', 'content', 'publish_date', 'status', 'user', 'categories')}),
    )
    def save_model(self, request, obj, form, change):
        #if 'owner' in form.changed_data:
        add_format_message(request, messages.INFO, mark_safe("好的, Please see <a href='/destination'>here</a> for further details"))
        add_format_message(request, messages.ERROR, mark_safe("出错啦, 这里是我们自定义的消息哦 (就是间隔有点大, 受不了)"))
        add_format_message(request, messages.DEBUG, "debug: 消息 <br> 第二行 <p> 第三行 ")
        super(PostCustomMessageAdmin, self).save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)

"""
#博客管理 ProxyModel
"""

#快速 建立管理视图Proxy (不必创建ProxyModel)
create_modeladmin(Post, PostQuickAdmin, name='postAdminCheck', verbose_name="Proxy 文章 导入导出 ( admin.py 中快捷加入)") #创建Site扩展管理视图
#正式 建立管理视图Proxy (创建ProxyModel )
admin.site.register(PostProxyModel, PostAdminCheck)

#快速建立保存消息视图
create_modeladmin(Post, PostCustomMessageAdmin, name='postCustomMessageAdminCheck', verbose_name="Proxy 文章 自定义保存消息 ( admin.py 中快捷加入)") #创建Site扩展管理视图