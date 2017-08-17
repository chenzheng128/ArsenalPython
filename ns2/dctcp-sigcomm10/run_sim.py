#!/usr/bin/env python
#coding:utf-8

"""
Controls the NS-2 simulation runs
"""

from datetime import datetime
import os, sys
import numpy as np
import argparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# sys.path.append(os.path.expandvars('$DCTCP_NS2/bin/'))
import ns_tools

PLOTS_DIR = './'

# 在同一绘图有关的参数, 例如 num_flows  congestion_alg, 考虑放在 .py 文件中

def get_env_value(default_val, env_name):
    """
    设定变量的默认值, 从环境变量中取值, 或获取默认值
    """
    ret_val=default_val;
    # print env_name, os.getenv(env_name)
    if os.getenv(env_name): 
        ret_val = os.getenv(env_name)
    #else:
        #os.popen("export %s=%s" % (env_name, default_val))
    print "debug: get_env_value: %s=%s" % (env_name, ret_val)
    return ret_val
def os_getenv(env_name):
    print "debug: os_get_env: %s=%s" % (env_name, os.getenv(env_name))
    return os.getenv(env_name)

# 初始值
# 流数量
num_flows=int(os_getenv("flownum"))
# 流启动间隔
tcpstartinterval=float(os_getenv("tcpstartinterval"))
# 绘图启动时间
tmin=float(os_getenv("tmin")) # 基本上 tmin在4秒时, 2个流就同步了


def make_fig_1():
    # if not os.path.exists(PLOTS_DIR):
    #         os.makedirs(PLOTS_DIR)
    # if not os.path.exists('output'):
    #         os.makedirs('output')

    for congestion_alg in ['TCP','DCTCP']:
        out_q_file = congestion_alg + '_q_size.out' 
        # run NS-2 simulation
        
        K = 20
        link_cap = '100Mbps'
        link_delay = '0.25ms'
        print "debug: running %s congestion_alg k=%d ..." % (congestion_alg, K)
        os.system('ns ../../run_sim.tcl {0} {1} {2} {3} {4} {5}'.format(congestion_alg, out_q_file,
                                                                      num_flows, K, link_cap,
                                                                      link_delay))
        # parse and plot queue size
        time, q_size = ns_tools.parse_qfile(os.path.join('./', out_q_file), t_min=tmin, t_max=9.0)
        plt.plot(time, q_size, linestyle='-', marker='', label=congestion_alg)

    ns_tools.config_plot('time (sec)', 'queue size (packets)', 'Queue Size over Time')
    ns_tools.save_plot('figure_1', PLOTS_DIR)
    plt.cla()


def make_fig_13():
    # if not os.path.exists(PLOTS_DIR):
    #         os.makedirs(PLOTS_DIR)
    # if not os.path.exists('output'):
    #         os.makedirs('output')
    for num_flows in [2, 20]:
        for congestion_alg in ['TCP','DCTCP']:
            out_q_file = congestion_alg + '_q_size.out' 
            K = 20
            link_cap = '100Mbps'
            link_delay = '0.25ms'
            # run NS-2 simulation
            print "debug: running %s congestion_alg k=%d ..." % (congestion_alg, K)
            os.system('ns ../../run_sim.tcl {0} {1} {2} {3} {4} {5}'.format(congestion_alg, out_q_file,
                                                                          num_flows, K, link_cap,
                                                                          link_delay))
            # parse and plot queue size
            time, q_size = ns_tools.parse_qfile(os.path.join('./', out_q_file), t_min=4.0, t_max=9.0)
            plt_label = congestion_alg + '_' + str(num_flows) + '_flows'
            # Compute the CDF
            sorted_data = np.sort(q_size)
            yvals=np.arange(len(sorted_data))/float(len(sorted_data)-1)
            plt.plot(sorted_data, yvals, linestyle='-', marker='', label=plt_label)

    ns_tools.config_plot('queue size (packets)', 'Cumulative Fraction', 'Queue Length CDF', legend_loc='upper center')
    ns_tools.save_plot('figure_13', PLOTS_DIR) 
    plt.cla()


def make_fig_14():
    # if not os.path.exists(PLOTS_DIR):
    #         os.makedirs(PLOTS_DIR)
    # if not os.path.exists('output'):
    #         os.makedirs('output')
    for congestion_alg in ['TCP', 'DCTCP']:
        throughputs = []
        # orginal step
        Ks = [i for i in range(1,2)]
        Ks += [i for i in range(4,11,3)]
        Ks += [i for i in range(15,35,5)]
        Ks += [i for i in range(40,101,10)]
      
        for K in Ks:
            out_q_file = congestion_alg + '_q_size.out'
            # run NS-2 simulation
            num_flows = 2
            link_cap = '100Mbps'
            link_delay = '10ms'
            # run NS-2 simulation
            print "debug: running %s congestion_alg k=%d ..." % (congestion_alg, K)
            os.system('ns ../../run_sim.tcl {0} {1} {2} {3} {4} {5}'.format(congestion_alg, out_q_file,
                                                                          num_flows, K, link_cap,
                                                                          link_delay))
            # Save throughput
            throughputs.append(1e-06 * ns_tools.parse_namfile(os.path.join('./',
                               'out.nam'), t_min=4.0, t_max=9.0))
        plt.plot(Ks, throughputs, linestyle='-', marker='o', label=congestion_alg)

    ns_tools.config_plot('K', 'Throughput (Mbps)', 'Throughput over K')
    ns_tools.save_plot('figure_14', PLOTS_DIR)
    plt.cla()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fig_1', action='store_true', help="reproduce figure 1 from the DCTCP paper")
    parser.add_argument('--fig_13', action='store_true', help="reproduce figure 13 from the DCTCP paper")
    parser.add_argument('--fig_14', action='store_true', help="reproduce figure 14 from the DCTCP paper")
    args = parser.parse_args()

    print "debug: lab start " , datetime.now()
    if (args.fig_1):
        make_fig_1()

    print "debug: " , datetime.now()
    if (args.fig_13):
        make_fig_13()

    print "debug: " , datetime.now()
    if (args.fig_14):
        make_fig_14()

    print "debug: lab end  " , datetime.now()

if __name__ == "__main__":
    main()

