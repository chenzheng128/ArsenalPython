# OTcl 官方文档

Source: https://www.isi.edu/nsnam/otcl/README.html

## 环境准备
*  安装 pawk `sudo pip install python-awk`

## How do I use it?

There's a quickstart tutorial to help you become familiar with OTcl syntax and style. It's included in the distribution.

* Tutorial https://www.isi.edu/nsnam/otcl/README.html
  - `tutorial.tcl`  官方文档代码
  - `tutorial-tcp.tcl` 参考分析 Agent/TCP 类

* `class_info.tcl` 通过命令 `[Class info instances]` 查看 OTcl 中的对象
  - `./class_info.sh > class_info.txt` 通过 `pawk` 将对象排序后存储, ns-2.35 标准对象为 660 个

## 参考
* CS558 Network Simulation using NS2: Tcl - 1 week: http://www.mathcs.emory.edu/~cheung/Courses/558/Syllabus/syl.html
* ns-by-exampels OTcl: The User Language: http://nile.wpi.edu/NS/otcl.html
  - `ns ../ns_by_example/basic02_ex-otcl.tcl`