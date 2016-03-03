# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import D01Article, D01Reporter, Question, Post

"""
Rest Tutorial 1 serialzation
http://www.django-rest-framework.org/tutorial/1-serialization/
"""

from rest_framework import serializers
from .models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


"""
SnippetSerializerRaw 用 Serializer来序列化, 手工完成很多代码, 和设计Form表单很类似
"""
class SnippetSerializerRaw(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=90)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance

"""
SnippetSerializer 简化版本, 使用ModelSerializer , 类似于ModelForm, 很多信息从model中取出
查看实际生成的代码
 (使用 ipython %paste)
$ ./manage.py shell
In [1]: %paste
>>> from d01_first_steps.serializers import SnippetSerializer
>>> serializer = SnippetSerializer()
>>> print(repr(serializer))
"""
class SnippetSerializer(serializers.ModelSerializer):
    class Meta:

        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style',)


"""
Tutorial4
* 改进UserSerializer4, 附加 snippets 列表 效果: http://localhost:8000/rest/users4/
* 改进SnippetSerializer4, 附加 owner _name, _email 信息 效果: http://localhost:8000/rest/snippets4/
"""
class SnippetSerializer4(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style', 'owner_name', 'owner_email')

    #tutorial4 将 owner 读出的属性 设置为 只读
    owner_name = serializers.ReadOnlyField(source='owner.username')
    owner_email = serializers.ReadOnlyField(source='owner.email')


class UserSerializer4(serializers.ModelSerializer):

    """
    在user中增加新的序列化字段
    """
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    class Meta:
        model = User
        #TODO 为什么不用从 HyperlinkedModelSerializer 继承, 一样可以使用 url 属性?
        fields = ('url', 'username', 'email', 'groups', 'snippets')

"""
tutorial5 using HyperlinkedModelSerializer
"""
class SnippetSerializer5(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Snippet
        fields = ('url', 'id', 'title', 'code', 'linenos', 'language', 'style',
                  'owner_name', 'owner_email', 'owner',
                  'hightlight', )

    #tutorial4 将 owner 读出的属性 设置为 只读
    owner_name = serializers.ReadOnlyField(source='owner.username')
    owner_email = serializers.ReadOnlyField(source='owner.email')
    # api form 只读
    #owner = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    # api form 可选编辑. 但由于 perform_save() 默认设置 owner 为创建用户, 所以这里的编辑可选择, 但是始终会设置为owner
    owner = serializers.HyperlinkedRelatedField(view_name='user-detail', queryset=User.objects.all())


    hightlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight5', format='html')

class UserSerializer5(serializers.HyperlinkedModelSerializer):

    """
    在user中增加snippets 连接,

    many=True表示 返回多个结果
    view_name='snippet-detail' 引用 snippet 链接
    """
    #url可以使用默认的设置指向 user-detail , 这里为了指向我们的 user-detail5 所以重载了一下
    #url = serializers.HyperlinkedIdentityField(view_name='user-detail')

    """
    snippets 控制, 只读--无api表单, 可写--有api表单
    """
    #只读 -- 关闭表单
    #snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
    #可写 -- 打开了 snippet 的 可编辑功能
    #TODO 希望实现 编辑 snippets 用户拥有的 snippets 反向更新, 但是未成功, 以后再试.
    #snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=False, queryset=Snippet.objects.all())
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'snippets')


"""
rest QuickStart
"""
class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = D01Article
        fields = ('headline', 'content', 'pub_date', 'reporter')

class ReporterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = D01Reporter
        fields = ('full_name', )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    在user中增加新的序列化字段
    """
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups',)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')



"""
Post Serializer
"""
class PostSerializer5(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'content', 'excerpt', 'publish_date', 'status', 'comments_count', 'view_count',
                  'alias', 'kyewords', 'description',
                  'user', )

