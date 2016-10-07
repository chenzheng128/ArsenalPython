NS by Example 代码
Source: http://nile.wpi.edu/NS/

执行程序前先 `cd output` 进入目录, 将生成文件留在 `output` 目录中便于跳过git版本管理

- Basics 基础
  * OTcl: The User Language
    + basic01: 简单的数学运算 (pow /mod) 例子
    + basic02: 简单的类 (Mom & Kid)
  * Simple Simulation Example
    + basic03: `ns ../basic03_ns-simple.tcl` 简单 simulation 拓扑(4个节点)例子, 生成 `out.nam`
- Post Simulation 结果分析
  * Trace Analysis Example
    + post01: `ns ../post01_ns-simple-trace.tcl` 写入 trace 文件 `out.tr` [文件格式说明](http://nile.wpi.edu/NS/analysis.html)
    + `../post01_trace2jitter.sh` 通过 `out.tr` 生成 `jitter.txt`
    + post02: `ns ../post02_red.tcl`
