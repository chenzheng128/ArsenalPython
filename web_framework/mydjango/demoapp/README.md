##学习 rest-framework 文档

###quickstart
Source: django rest framework quickstart http://www.django-rest-framework.org/tutorial/quickstart/

* 创建了Article, Reporter, User, Group 等 Serializer (serializer.py), 继承的 HyperlinkedModelSerializer 很帅
* 创建了Article, Reporter, User, Group 等 ModelViewSet (view.py)  
* 使用router.url 注册 router.register 到urlpattern中 (url.py)

ModelViewSet 如此高效, 是由于集成了 5个 ModelView ( 参 tutorial/3-class-based-views )

```
class ModelViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
```


###tutorial 1-3
Source: http://www.django-rest-framework.org/tutorial/1-serialization/

* 1-serialization/: 创建Snippet model(models.py), 以及 SnippetSerializer 原始版本Raw与简化版本(serializer.py). 使用原始的JSONResponse (view.py) 实现了列表显示 参: http://localhost:8000/rest/snippets/
* 2-requests-and-responses/: 使用 @api_view 简化了reponse view的创建, 并且requests的数据获取也简化为了 request.data: 参 http://localhost:8000/rest/snippets2/
* 3-class-based-views/: 使用模板类一步步简化, 最后的 generics.ListCreateAPIView 浓缩为 几行代码. 

ListCreateAPIView 如此高效, 是由于集成了2个ModleView

```
class ListCreateAPIView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        GenericAPIView):
```

一般从 Retrieve/List/Generic 等 APIView (generics.py) 继承即可. 如果不爽,
 可以从 Retrieve/List/ModelMixin (mixi)继承  

### Tutorial 4: Authentication & Permissions
source: http://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/

原有的认证与权限为IsAuthenticatedOrReadOnly, 它局限在只要用户登录后, 就拥有对所有对象的权限

改进后的权限控制将权限收回到 创建者 即 owner 手中
* Code snippets are always associated with a creator.
* Only authenticated users may create snippets.
* Only the creator of a snippet may update or delete it.
* Unauthenticated requests should have full read-only access.

需要的步骤包括
* 为解决认证问题,在 snippet model.py 中引入了 owner = models.ForeignKey('auth.User', related_name='snippets')
* 覆盖 snippet model.py 的 save() 操作, 增加业务处理, 生成 self.highlighted = highlight(self.code, lexer, formatter) 
* 改进UserSerializer4, 附加 snippets 列表 效果: http://localhost:8000/rest/users4/
* 改进SnippetSerializer4, 附加 owner _name, _email 信息 效果: http://localhost:8000/rest/snippets4/
* 创建 class IsOwnerOrReadOnly (permissions.py), 应用在 permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

### Tutorial 5: Relationships & Hyperlinked APIs
source: http://www.django-rest-framework.org/tutorial/5-relationships-and-hyperlinked-apis/

* 在 viesw.py 中增加 api_root() 函数 def api_root(request, format=None):
* 增加 代码Highlite显示类 class SnippetHighlight(generics.GenericAPIView) 
* 改进 SnippetSerializer/UserSerializer5, 使用 HyperlinkedModelSerializer 类, 
以及 HyperlinkedIdentityField 从主键创建链接  HyperlinkedRelatedField 从关联键位创建链接
* 在 url.py 中定义好 对于的 pattern 名称, 便于在 serializer.py 中的 HyperlinkedIdentityField 进行引用 

注意: url 参数默认会引用链接名称为  '{model_name}-detail',
例如 'snippet-detail' and 'user-detail'.
Our snippet and user serializers include 'url' fields that by default will refer to '{model_name}-detail',
 which in this case will be 'snippet-detail' and 'user-detail'.

##学习 django 官方文档 (1.8)
Source: https://docs.djangoproject.com/en/1.8/intro/overview/