scratch 目录

## Tutorial 例子
 以 my[first|second|third等].cc 为命名格式
 * 

## manual 例子
 以 mn[0-9]-<orignal-source>.cc 为命名格式
 其中 mn 为 manual 缩写 [0-9] 为章节小标题, 例如 mn072 即 1.07.2 章小结. 因为手册都在第一大章中，所以 1 忽略了。
 
* 01 Organization 3
* 02 RandomVariables 4
* 03 HashFunctions 9
* 04 EventsandSimulator 11
* 05 Callbacks 13
   - 设置与获取对象属性 `./waf --run mn172-main-attribute-value`, copy from "src/point-to-point/examples/main-attribute-value.cc"
* 06 Objectmodel 22
* 07 ConfigurationandAttributes 26
   - 使用 Callback 函数 `./waf --run mn153-main-callback`
* 08 Objectnames 43
* 09 Logging 43
* 10 Tracing 48
  - 使用 ConfigTracing `./waf --run mn103-tcp-large-transfer`, 原始的运行并激活日志方法 "NS_LOG="TcpLargeTransfer=*" ./waf --run tcp-large-transfer"
  - 修改 myseven2 `./waf --run mn103-myseventh2`
* 11 DataCollection 64
  - `src/stat/examples` 下的一些例子 
    + doubleProbe 例子 `NS_LOG="DoubleProbeExample=all" ./waf --run double-probe-example`
    + gnuplot helper 例子 `NS_LOG="GnuplotHelperExample=all" ./waf --run gnuplot-helper-example && sh gnuplot-helper-example.sh && open gnuplot-helper-example.png`
  - 11.3 Proble
  - 我们的 Uinteger32Probe 例子: `./waf --run mn103-myseventh2 `
* 12 StatisticalFramework 89
* 13 RealTime 97
* 14 Helpers 99
* 15 MakingPlotsusingtheGnuplotClass 99
* 16 UsingPythontoRunns-3 107
* 17 Tests 112
* 18 Support 128

  
 
 
