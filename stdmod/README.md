#Python Stand Library Demo

 stdmod: python 标准库使用参考代码


- json: json dump/load 操作
- requests: 爬虫例子（需要额外安装 lxml 库）
- socket: 
    * pymotw:
        - unix domain socket 服务与客户端: `python ./socket_echo_server_uds.py` `python ./socket_echo_client_uds.py [filepath.socket]` 
- unittest: using noise test all classes in this folder

## unittest 单元测试
对于  mylib 实现了 `100%` 的 converage 测试 
- `mylib` unittest 用到的lib类  (mock并不包含在 python2.7 stdmod 当中, 为了方便将它放在这里)
    - `test` testcase
        - sub 子目录测试
        - assert.py 常用的 assert 函数
        - skip_test_n_expect_failure.py 跳过一些测试类 
        - test_req_mock.py mock 作 requests 库测试, 实现了 @mock.patch
        - test_rm_mock.py  mock 作 os.rm 库测试
        - test_rm_nomock.py os.rm 库普通测试
      
mock文档: 
- Mock RmService 英文版本: https://www.toptal.com/python/an-introduction-to-mocking-in-python
- Python Magic Methods http://www.ironpythoninaction.com/magic-methods.html


 
 单元测试注意, 测试类要以 test_ 开头, 否则 nose 不会检测到
 
 起module名称的时候要注意. 如果取成 mail , mock 等和系统module一样名字, 很容易悲惨的遇到 no mudule 错误
 
 # Python Magic Methods
 