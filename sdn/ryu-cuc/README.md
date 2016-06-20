CUC代码目录

## 主要目录
- `book` Ryu Book 代码与文档 
- `docs` 官方代码与文档


#  `ryu/tests` 测试

## unit 单元测试

运行 nose unittest shell 代码 
``` 
PYTHONPATH=. ./cuc/run_tests_cuc.sh 
``` 

(TODO: mock nose 进一步学习)

执行特定目录 `sample`  `app` 的单元测试
```
cd ryu/ryu/tests/unit
nosetests -v sample app  

----------------------------------------------------------------------
Ran 179 tests in 0.760s

FAILED (errors=1) # 一个测试不通过 (在 pycharm 中可用  #eq_("a", os.getcwd(), os.getcwd()) 打印当前目录等信息) 
```

执行特定文件 `app/test_ofctl_rest.py` 的单元测试
```
nosetests -v app/test_ofctl_rest.py

----------------------------------------------------------------------
Ran 168 tests in 0.777s

OK # 所有测试通过
```

## switch 交换机测试

对 Book 12. 测试 中的测试进行了简化. test-switch-dir cuc 中仅保留了少数几个测试文件.

首先在mininet vm启动 `run_mininet.py` mininet 拓扑网络 (默认ip使用 127.0.0.1 和book文档保持一致便于命令测试, 不使用我们自定义的192.168.57 ), 然后运行 `tester.py`
```
cd RYU_HOME
sudo python ryu/tests/switch/run_mininet.py
PYTHONPATH=. python ./bin/ryu-manager --test-switch-dir cuc/tests/switch/of13/match ryu/tests/switch/tester.py
``

