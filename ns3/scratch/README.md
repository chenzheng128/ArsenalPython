## scratch 目录代码
 * tcp参数实验 `./waf --run "my-tcp-variants-comparison"`

## Tutorial 例子
 以 my[first|second|third等].cc 为命名格式
 * 

## manual 例子
 以 mn[0-9]-<orignal-source>.cc 为命名格式
 其中 mn 为 manual 缩写 [0-9] 为章节小标题, 例如 mn072 即 1.07.2 章小结. 因为手册都在第一大章中，所以 1 忽略了。
 
* 01 Organization 3
* 02 Random Variables 4 随机变量
* 03 HashFunctions 9 Hash 函数
* 04 Events and Simulator 11 (大部分内容为空)
* 05 Callbacks 13 回调函数
   - 设置与获取对象属性 `./waf --run mn172-main-attribute-value`, copy from "src/point-to-point/examples/main-attribute-value.cc"
* 06 Object model 22 对象模型的要素 ( 内存管理 + 聚合 ) 
* 07 Configuration and Attributes 26 配置与属性
   - 使用 Callback 函数 `./waf --run mn153-main-callback`
* 08 Object names 43 (空内容)
* 09 Logging 43 日志记录, 非 debug 模式不输出
* 10 Tracing 48 使用 callback 记录数据
  - 使用 ConfigTracing `./waf --run mn103-tcp-large-transfer`, 原始的运行并激活日志方法 "NS_LOG="TcpLargeTransfer=*" ./waf --run tcp-large-transfer"
  - 修改 myseven2 `./waf --run mn103-myseventh2`
* 11 DataCollection 64 使用 probe 记录数据
  - `src/stat/examples` 下的一些例子 
    + doubleProbe 例子 `NS_LOG="DoubleProbeExample=all" ./waf --run double-probe-example`
    + gnuplot helper 例子 `NS_LOG="GnuplotHelperExample=all" ./waf --run gnuplot-helper-example && sh gnuplot-helper-example.sh && open gnuplot-helper-example.png`
  - 11.3 Proble 
  - 我们的 Uinteger32Probe 例子: `./waf --run mn113-myseventh2 `
* 12 Statistical Framework 89 统计框架
  - 运行 wifi 例子: `cd examples/stats/ && sh wifi-example-db.sh && open wifi-default.eps`
* 13 RealTime 97 (Linux 专用)
* 14 Helpers 99 使用Helper绘图
* 15 Making Plots using the Gnuplot Class 99
  - 2d与3d 绘图例子 `./waf --run src/stats/examples/gnuplot-example;`  
     + `gnuplot plot-2d.plt && open plot-2d.png; `
     + `gnuplot plot-2d-with-error-bars.plt && open plot-2d-with-error-bars.png;` 
     + `gnuplot plot-3d.plt && open plot-3d.png`
* 16 Using Python to Runns-3 107 (Linux 下使用 Python)
* 17 Tests 112 测试
  - 查看测试项目 `./test.py  --list --nowaf`
  - 运行某个单元测试并生成 html 报告  `./test.py --suite=propagation-loss-model --html=nightly.html && open nightly.html`
  - 查看测试种类 `./test.py --kinds`
  - 仅运行unit或example `./test.py --constrain=example`  
  - 跳过 waf 编译 `./test.py -s buffer --nowaf`
  - 运行某个suit `./test.py -s time --nowaf`
  - 运行某个例子 `./test.py --example second --nowaf` 
* 18 Support 128 创建 ns-3 新 model

  
 
 
