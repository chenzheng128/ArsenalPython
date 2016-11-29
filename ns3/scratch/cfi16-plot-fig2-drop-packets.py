#!/usr/bin/env python
#coding: utf-8
# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api

# Source https://plot.ly/matplotlib/bar-charts/
#

import matplotlib.pyplot as plt
# import plotly.plotly as py

dictionary = plt.figure()

tcp_vars = [u'Reno', u'Vegas', u'HS', u'STCP', 'W+', 'BIC', 'CUBIC', 'YeAH']
drop_packets = [2492, 6, 3102, 4872, 2965, 3675, 0, 1682]


# ax.set_title('axes title')
width =  0.5
plt.bar(range(len(tcp_vars)), drop_packets, width, align='center',)
plt.xticks(range(len(tcp_vars)), tcp_vars)
plt.title("Figure 2: Total number of dropped packets")
plt.xlabel('TCP variants')
plt.ylabel('number of dropped packets')
plt.axis([-1, 8, 0, 14000])

plt.show()
#plot_url = py.plot_mpl(dictionary, filename='mpl-dictionary')
