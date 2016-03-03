#Python Web Framework 开发demo


Python的web框架： https://wiki.python.org/moin/WebFrameworks

##json新闻渲染（前端）
使用json数据（网易新闻）生成新闻页面

代码位置
```
cd jsonNews
```

##django 众筹网站(前后端)

REF: Django 基础教程 (自强学堂 涂伟忠 ) http://www.ziqiangxuetang.com/django/django-tutorial.html

代码位置
```
cd cuczhongchou
```

用git管理学习代码(REAMDE文档保持在master中更新，其他代码保存在step0x【本章起始代码，便于开始此章实验】, step0x-done 【本章完成代码，便于查看效果】) (

备注：
这些代码的生成方式为：完成上一章step01后，会git checkcout step02; git checkout step02-done;本章代码都会commit在step02-done分支中，学习查看)

文档的README.md的更新方式可以git checkout master 之后复制回来。这样就不必使用任何merge操作。

最后分支效果图应该为(done中含commit代码，其他分支仅当tag使用)

```
    step01 -> step02-done -> step03-done -> step04-done ... 
          \               \               \
           -> step02       -> step03      -> step04
```


##django 官方文档 入门

完成了官方文档 1.8 (https://docs.djangoproject.com/en/1.8/) 中的 frist_step内容, 包含两部分
* Overview (类似 QuickStart) 中采用的Model是 Report记者, Article文章
* Tutorial 6j节内容设计Model为 Poll投票, Question问题-Choice选择, (无前台)主要包括模型的创建, 模板, 测试 (未完全通过, 考虑更换为mysql数据库) 等. (前台地址: http://localhost:8000/d01/ )

在汉化问题上, 参考了  django 博客汉化方法 (http://lishiguang.iteye.com/blog/1328986), 引入了一些博客Model, 包括 Category文章分类, Tag文章标签, Post发布文章等 

代码位置
```
cd cuczhongchou/d01_first_step
```



##web.py

REF: web.py 0.3 新手指南 http://webpy.org/tutorial3.zh-cn