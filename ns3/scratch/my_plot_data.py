#coding: utf-8
#!env python
# pyenv shell anaconda2-2.5.0
# python scratch/my_plot_data.py seventh-cwnd-count.dat
import sys
import matplotlib.pyplot as plt
import numpy as np

if len(sys.argv) < 2:
    print "Usage: %s <filename1.dat> <filename2.dat>" % sys.argv[0]
    print "Example: %s ../seventh-cwnd-count.dat" % sys.argv[0]
    sys.exit()

for this_file in sys.argv[1:]: # support multiple file
    plt.clf() # 清除上一次绘图
    arr = np.genfromtxt(this_file)
    print ("读入了数据文件 %s" % this_file)
    plt.plot(arr[:,0], arr[:,1], )
    plt.title(this_file)
    png_filename = "%s.%s" % (this_file, 'png')
    plt.savefig(png_filename) # 保存文件
    print ("生成了图形文件 %s" % png_filename)
    if len(sys.argv) == 2: # 如果仅有一个图表则显示, 否则只是批量生产png文件
        plt.show()
