# -*- coding: utf-8 -*-
from django.http.request import HttpRequest
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.core.handlers.wsgi import WSGIRequest
from django.core import urlresolvers
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.utils import timezone
from rest_framework.renderers import JSONRenderer

from .models import *
from .serializers import *
from django.contrib.auth.models import User



"""
创建json接口
http://www.django-rest-framework.org/tutorial/1-serialization/
"""

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *

"""
手工方式创建的JSONReponse
仅引用了 JSONRenderer JSONParser, 配合Serializer使用
"""
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def snippet_list(request):
    """
    手工方式创建的代码Snippets List
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)

"""
snippet_list2  使用 @api_view 简化
好像也没简化多少, 只是不再需要用到 JSONReponse了
  也不再用到 data = JSONParser().parse(request)
    直接使用 request.data 就可以

tutorial02 里面的这个没试验成功. api_view 没装饰上去, 以后再调试
"""

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Snippet
from .serializers import SnippetSerializer
import rest_framework.renderers


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAdminUser,]) #覆盖global settings.py 中的DEFAULT_PERMISSION_CLASSES
def snippet_list2(request, format=None):
    """
    使用 @api_view 简化的List \n
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)
        #return HttpResponse("snippet_list2")

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail2(request, pk, format=None):
    """
    Retrieve, update or delete a snippet instance.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
"""

"""
tutorial3 class base view
http://www.django-rest-framework.org/tutorial/3-class-based-views/
"""


"""
使用APIView类简化
"""

from rest_framework.views import APIView
class SnippetList(APIView):

    """
    使用APIView类简化 \n
    List all snippets, or create a new snippet.
    """

    permission_classes = (permissions.AllowAny, ) #覆盖global settings.py 中的DEFAULT_PERMISSION_CLASSES

    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SnippetDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
 snippet 使用 多个模板类 简化
"""
from rest_framework import mixins
from rest_framework import generics

class SnippetListB(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    """
     使用 多个模板类  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView 简化的 List
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class SnippetDetailB(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



"""
 snippet 最简化版本
"""
class SnippetListC(generics.ListCreateAPIView):
    """
    最简化版本 继承 generics.ListCreateAPIView
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

class SnippetDetailC(generics.RetrieveUpdateDestroyAPIView):
    """
    最简化版本 继承 RetrieveUpdateDestroyAPIView \n
    权限控制使用 IsAuthenticatedOrReadOnly 类, 只要是个登录用户就能随便改
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


"""
Tutorial 4
http://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/
 使用 UserSerializer 来展示用户的snippets
"""


from .permissions import IsOwnerOrReadOnly


class SnippetListD(generics.ListCreateAPIView):
    """
    增加了 创建时(perform_create) 设置 owner 属性

    追加了权限控制, 要认证才能发东西

    *这个不行:
    http POST http://127.0.0.1:8000/rest/snippets3D/ code="print 789"

    *这个才可以:
    http -a nic:nic POST http://127.0.0.1:8000/rest/snippets3D/ code="print 789"
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer4

    # 可以打开认证了 TODO: 自定义的 IsOwnerOrReadOnly 合适发生作用?
    #permission_classes =  (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )
    permission_classes =  ( permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )

    #tutorial 4 创建时, 追加owner信息
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetailD(generics.RetrieveUpdateDestroyAPIView):
    """
    追加IsOwnerOrReadOnly 权限控制, 只有owner才能够进行编辑操作的方法了 \n
    可以对比 snippets3C 来查看区别, 3C 只要是登录用户就可以删除东西

    """
    permission_classes =  ( permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer4

class UserListD(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer4


class UserDetailD(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer4

"""
Tutorial5 relationships-and-hyperlinked-apis
http://www.django-rest-framework.org/tutorial/5-relationships-and-hyperlinked-apis/
"""
from rest_framework.reverse import reverse
@api_view(('GET',))

def api_root5(request, format=None):
    """
    自定义的 api_root(request, format=None):

    format 参数: json/html

    使用reverse('user-list', request=None, format=format),

    * 非rest的reverse() 不用传入 request, 由于其只生成 /url即可,
    * 但是rest的reverse() 用传入 request, 由于其要生成 完整的 http://ip/url 链接
    """

    return Response({

        'users': reverse('user-list5', request=request, format=format),
        'snippets': reverse('snippet-list5', request=request, format=format),
        'z-snippets-fake-no-request':
                reverse('snippet-list5', request=None, format=format)
    })


from rest_framework import renderers
from rest_framework.response import Response

"""
    由于其实只想要 snippet 当中的 单个属性 highlighted 的数据

    所以不继承 RetrieveModelMixin 类. 其 get 方法默认返回的是整个对象Model的serrialzer化 json数据.
     ```
     def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
     ```

    而是重写了 get类, 也不需要 serializer, 仅返回单个属性 Response(snippet.highlighted)

"""
class SnippetHighlight5(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        #print "debug SnippetHighlight5 get ", snippet.highlighted
        return Response(snippet.highlighted)


class SnippetList5(generics.ListCreateAPIView):
    """
    ##SnippetList5
    using SnippetSerializer5 HyperlinkedModelSerializer
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer5


    # 可以打开认证了 TODO: 自定义的 IsOwnerOrReadOnly 合适发生作用?
    #permission_classes =  (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )
    permission_classes =  ( permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )

    #tutorial 4 创建时, 追加owner信息
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetail5(generics.RetrieveUpdateDestroyAPIView):
    """
    SnippetDetail5
    """
    permission_classes =  ( permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer5

class UserList5(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer5


# 要使用 正确的 RetrieveUpdateAPIView 才能编辑
class UserDetail5(generics.RetrieveUpdateAPIView):
    permission_classes =  ( permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )
    queryset = User.objects.all()
    serializer_class = UserSerializer5

    #TODO 希望通过重载能够实现 用户拥有的 snippets 反向更新, 但是未成功, 以后再试.
    def update(self, request, *args, **kwargs):
        print "UserDetail5 成功重载了 update"
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        print request.data
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        print "UserDetail5 成功重载了 perform_update"
        print serializer.data
        serializer.save()


"""
django rest framework quickstart http://www.django-rest-framework.org/tutorial/quickstart/
"""

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .models import D01Article, D01Reporter
from .serializers import UserSerializer, GroupSerializer, ArticleSerializer, ReporterSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = D01Article.objects.all().order_by('-pub_date')
    serializer_class = ArticleSerializer


class ReporterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = D01Reporter.objects.all()
    serializer_class = ReporterSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


"""
    Tutorial 03 file:///Users/chen/coding/documentations/django-docs-1.8-en/intro/tutorial03.html
"""

"""
    版本1: 手工实现
"""


def index2(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([p.question_text for p in latest_question_list])
    # #return HttpResponse(output)
    template = loader.get_template('d01_first_steps/polls_index.html')
    context = RequestContext(request, {
        'latest_question_list': latest_question_list,
    })
    return HttpResponse(template.render(context))


def detail(request, question_id):
    # return HttpResponse("You're looking at question %s." % question_id)

    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404(u"找不到这个投票问题")

    # 上面代码的简化版本
    question = get_object_or_404(Question, pk=question_id)

    return render(request, 'd01_first_steps/polls_detail.html', {'question': question})


def results(request, question_id):
    # 简单模拟实现
    # response = "You're looking at the results of question %s."
    # return HttpResponse(response % question_id)

    # DAO操作
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'd01_first_steps/polls_results.html', {'question': question})


def vote(request, question_id):
    # 简单实现了此函数
    # return HttpResponse("You're voting on question %s." % question_id)

    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):  # 处理两个异常 KeyError 没有post choice, NotExist 找不到当前投票
        # Redisplay the question voting form.
        return render(request, 'd01_first_steps/polls_detail.html', {
            'question': p,
            'error_message': "请选择一个选项 ",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(urlresolvers.reverse('polls:results', args=(p.id,)))


"""
版本2 : 使用通用模板 file:///Users/chen/coding/documentations/django-docs-1.8-en/intro/tutorial04.html#amend-views
"""


class IndexView(generic.ListView):
    print "debug: IndexView"
    template_name = 'd01_first_steps/polls_index.html'
    context_object_name = 'latest_question_list'

    # 原来的queryset ,没有logic判断
    # def get_queryset(self):
    #    """Return the last five published questions."""
    #    return Question.objects.order_by('-pub_date')[:5]

    # 新的query_set 增加时间判断
    def get_queryset(self):

        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    print "debug: DetailView"
    model = Question
    template_name = 'd01_first_steps/polls_detail.html'


    #过滤某些不希望显示的 Question
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'd01_first_steps/polls_results.html'


"""
#  Overview https://docs.djangoproject.com/en/1.8/intro/overview/
"""


def year_archive(request, year):
    a_list = D01Article.objects.filter(pub_date__year=year)
    context = {'year': year, 'article_list': a_list}
    return render(request, 'd01_first_steps/year_archive.html', context)


### 一个默认的snoop页面，便于调试
def snoop(request):
    # request = WSGIRequest()
    for key, value in request.POST:
        print key, value
    # raise ValueError("Got Some Error");
    return HttpResponse("snoop Response1");

#
#

# Create your views here.
