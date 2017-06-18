
## The Manual (formerly Notes and Documentation)0.1

Source: https://www.isi.edu/nsnam/ns/doc/everything.html

### Nov 5, 2011 (ns-2.35)

http://www-nrg.ee.lbl.gov/ns/ ©../copyright.html is LBNL's Network Simulator [24]. The simulator is written in C++; it uses OTcl as a command and configuration interface.  v2 has three substantial changes from v1: (1) the more complex objects in v1 have been decomposed into simpler components for greater flexibility and composability; (2) the configuration interface is now OTcl, an object oriented version of Tcl; and (3) the interface code to the OTcl interpreter is separate from the main simulator.

Ns documentation is available in html, Postscript, and PDF formats. See http://www.isi.edu/nsnam/ns/ns-documentation.html for pointers to these.

* 1. Introduction 
    - `ns ../01-1-intro.tcl` 运行一个简单例子 tcp + udp
* 3. Introduction
    - 3.2 Code Overview: `./tclcl-1.20/tcl-object.tcl ...`
    - 3.5 Class TclClass: `RenoTcpClass` `TraceClass` 继承于 TclClass
    - 3.6 Class TclCommand: 在 ns 命令行下可执行的命令
        + 查看 ns 版本 % `ns-version`, 随机数
    - 

