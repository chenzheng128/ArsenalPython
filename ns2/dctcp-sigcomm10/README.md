## 准备
按照 ../dctcp 准备 ns-2.35 dctcp ns, 并顺利运行 `dctcp-dumbbell.tcl`, 支持激活 dctcp 的 ns

## 运行

方式1
* `make run` 默认参数运行所有Fig
* `make run1` 默认参数运行Fig1

方式2
* `cd output/ ; ../run.sh` 多组参数运行比较

## 修改

Revisied from https://github.com/sibanez12/dctcp-ns2.git
经测试 ns-2.35 与 原始代码 ns-2.34 的运行效果相同

主要修改为:
* 所有输出放到 output 目录下
* /bin 中的代码不再使用, 仅作参考
* run.sh 代码移动至 make run 下

Reproduce the Results
=====================

The results are designed to be reproduced on a machine running Ubuntu 14.04. 
It is recommended to run the simulations on a Google Compute Engine instance 
to ensure maximum consistency and reproducibility. Below are the instructions
to reproduce:

(Optional) Google Compute Engine Instance Setup
-----------------------------------------------

This method requires that you have a Google Cloud account and associated 
billing account (or free trial) set up.

1. Navigate to your [Google Cloud Console](https://console.cloud.google.com) 
and click "Compute Engine > Images" on the left hand side.

2. Search for the ubuntu-1404 image and select it. Click "CREATE INSTANCE".

3. Choose a name for your instance (e.g. dctcp-ns2). Choose your desired zone 
to host your instance. Choose 4 vCPUs as the machine type. Make sure to check
the box to allow HTTP traffic. Click "Create".

Installation and Reproduction Steps:
------------------------------------

1. Install git and make: 
`$ sudo apt-get -y install git make`

2. Clone the repository:
`$ git clone https://github.com/sibanez12/dctcp-ns2.git`

3. Install the dependencies (this will take about 8 minutes):
`$ cd dctcp-ns2 && make`

4. Reproduce the results (this will take about 5 minutes):
`$ ./run.sh`

The plots will be saved in the plots/ directory. When the simulations are 
complete and the plots have been produced, an HTTP server will be started 
up automatically (may need to enter sudo password).

5. Please identify the External IP address of the machine you are running the 
simulations on and navigate to http://<IP_ADDRESS> or to http://localhost
if you are running on a local machine. Click on a link to view the
corresponding figure. 


Additional Notes
----------------

You can use the run_sim.py script to create figures individually, but you
will need to source the settings.sh script first. 

Run, `$ ./run_sim.py --help` for usage information.


