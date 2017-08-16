#!/usr/bin/env python

"""
Controls the NS-2 simulation runs
"""

import os, sys
import numpy as np
import argparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# sys.path.append(os.path.expandvars('$DCTCP_NS2/bin/'))
import ns_tools

PLOTS_DIR = 'output/'

def make_fig_1():
    if not os.path.exists(PLOTS_DIR):
            os.makedirs(PLOTS_DIR)
    if not os.path.exists('output'):
            os.makedirs('output')
    for congestion_alg in ['TCP','DCTCP']:
        out_q_file = congestion_alg + '_q_size.out' 
        # run NS-2 simulation
        num_flows = 2
        K = 20
        link_cap = '100Mbps'
        link_delay = '0.25ms'
        os.system('ns run_sim.tcl {0} {1} {2} {3} {4} {5}'.format(congestion_alg, out_q_file,
                                                                      num_flows, K, link_cap,
                                                                      link_delay))
        # parse and plot queue size
        time, q_size = ns_tools.parse_qfile(os.path.join('output/', out_q_file), t_min=4.0, t_max=9.0)
        plt.plot(time, q_size, linestyle='-', marker='', label=congestion_alg)

    ns_tools.config_plot('time (sec)', 'queue size (packets)', 'Queue Size over Time')
    ns_tools.save_plot('figure_1', PLOTS_DIR)
    plt.cla()


def make_fig_13():
    if not os.path.exists(PLOTS_DIR):
            os.makedirs(PLOTS_DIR)
    if not os.path.exists('output'):
            os.makedirs('output')
    for num_flows in [2, 20]:
        for congestion_alg in ['TCP','DCTCP']:
            out_q_file = congestion_alg + '_q_size.out' 
            K = 20
            link_cap = '100Mbps'
            link_delay = '0.25ms'
            # run NS-2 simulation
            os.system('ns run_sim.tcl {0} {1} {2} {3} {4} {5}'.format(congestion_alg, out_q_file,
                                                                          num_flows, K, link_cap,
                                                                          link_delay))
            # parse and plot queue size
            time, q_size = ns_tools.parse_qfile(os.path.join('output/', out_q_file), t_min=4.0, t_max=9.0)
            plt_label = congestion_alg + '_' + str(num_flows) + '_flows'
            # Compute the CDF
            sorted_data = np.sort(q_size)
            yvals=np.arange(len(sorted_data))/float(len(sorted_data)-1)
            plt.plot(sorted_data, yvals, linestyle='-', marker='', label=plt_label)

    ns_tools.config_plot('queue size (packets)', 'Cumulative Fraction', 'Queue Length CDF', legend_loc='upper center')
    ns_tools.save_plot('figure_13', PLOTS_DIR) 
    plt.cla()


def make_fig_14():
    if not os.path.exists(PLOTS_DIR):
            os.makedirs(PLOTS_DIR)
    if not os.path.exists('output'):
            os.makedirs('output')
    for congestion_alg in ['TCP', 'DCTCP']:
        throughputs = []
        Ks = [i for i in range(1,11,1)]
        Ks += [i for i in range(15,35,5)]
        Ks += [i for i in range(40,101,10)]
        for K in Ks:
            out_q_file = congestion_alg + '_q_size.out'
            # run NS-2 simulation
            num_flows = 2
            link_cap = '100Mbps'
            link_delay = '10ms'
            # run NS-2 simulation
            os.system('ns run_sim.tcl {0} {1} {2} {3} {4} {5}'.format(congestion_alg, out_q_file,
                                                                          num_flows, K, link_cap,
                                                                          link_delay))
            # Save throughput
            throughputs.append(1e-06 * ns_tools.parse_namfile(os.path.join('output/',
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

    if (args.fig_1):
        make_fig_1()

    if (args.fig_13):
        make_fig_13()

    if (args.fig_14):
        make_fig_14()


if __name__ == "__main__":
    main()

