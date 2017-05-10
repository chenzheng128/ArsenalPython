

## Videos on Modeling with Gurobi and Python

三个 python webinar 的代码资料

### Env 运行环境
```
pyenv version
# anaconda2-4.3.1
conda list gurobi
# gurobi                    7.0.2                    py27_0

Jupyter motebooks # 启动 notebook 环境
```
### 其他资料 Slides 参考 Evernote: gurobi  Webinar  Python

### Python I: Introduction to Modeling with Python

This 55 minute video, part one of a three-part series, presents an introduction to using Python, Gurobi and Jupyter Notebooks. It covers the basics of model-building, including working with decision variables, constraints, objective function, sums and for-all loops.

* demo1 读文件解模型
* demo2 创建简单模型
* demo3 工厂规划 (车床使用 货物存储 销售等)

### Python II: Advanced Algebraic Modeling with Python and Gurobi

This one-hour video, part two of a three-part series, covers more advanced topics including data structures and loops, sum and for-all expressions, working with large data sets and building large-scale, high-performance applications using the Gurobi Python interface.

Code Examples - http://www.gurobi.com/resources/examples/example-models-overview •

Functional(code)examples
 • Modelingexamples

* netflow.ipynb 网络货物流问题 mcf
* workforce.ipynb 工人排班问题

### Python III: Optimization and Heuristics

This one-hour video, part three of a three-part series, covers one capability of MIP that is often overlooked: its ability to find and subsequently improve good quality solutions to exceedingly difficult problems. This webinar, which builds on the ideas presented in the last Python webinar, will focus on techniques for using the Gurobi MIP solver as a heuristic.

使用 Gurobi 作为 heuristic 算法解问题

* Optimization_and_Heuristics.ipynb 视频配套 notebook (禁用了 inline 绘图)
* mining35.py 备份原始 mining.py 代码, 需要在 python35 下运行
* mining.py 原始代码, 需要修改为 python27 下执行
* tsp2.py 旅行商问题代码
