#豆瓣数据挖掘

## 安装 
MongoDB 使用 Robo 3T 客户端 （ 待更换， 因为暂时不支持 Query 功能 ）

## 运行环境
```
Python 2.7.13 :: Anaconda 4.3.1 (x86_64)
MongoDB: 4.0.1 客户端： NoSQLBooster 
```

## 运行方法
启动 mongodb, 参考 http://www.runoob.com/mongodb/mongodb-query.html 使用命令行查询
执行 `python douban_main.py` 循环抓取 douban 即将上映数据， 存放至 test 库当中

## 依赖类
* `douban_client.py` 豆瓣爬虫的 api 类 ，获取 json 数据（201808：douban API 错误由 403 修改为 400）
* `douban_mongo.py` 豆瓣爬虫的 model 类， 存储数据至 mongo 中


## 基础程序
```
mongo_demo.py mongodb 的参考持久化代码参考测试, 参考官网: https://docs.mongodb.org/getting-started/python/ 在 test 库中插入 restaurants 数据
```

