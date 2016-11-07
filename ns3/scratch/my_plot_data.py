#coding: utf-8
#!env python
# 进入 anaconda 环境
# pyenv shell anaconda2-2.5.0  / pyenv shell anaconda2-2.4.1
#

# 单绘图
# python scratch/my_plot_data.py seventh-cwnd-count.dat
#
# 独立 多绘图模式 (适合一种模型下的不同类型图表)
# python scratch/my_plot_data.py TcpVariantsComparison-TcpNewReno-*.txt
#
# merge 多绘图模式 (适合不同模型下的同一类型图表对比)
# python scratch/my_plot_data.py --merge TcpVariantsComparison-*-cwnd.txt

import sys
import matplotlib.pyplot as plt
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='对 ns3 tracing 作绘图处理')

# api add_argument() https://docs.python.org/2/library/argparse.html#module-argparse
parser.add_argument('--merge', action='store_true', help='是否叠加绘图结果')
parser.add_argument('filenames', metavar='filename', nargs='+',
                    help='要处理的文件名')
# parser.parse_args(args=['--merge', 'a.txt', 'b.txt'])

args = parser.parse_args()

# if len(sys.argv) < 2:
#     print "Usage: %s <filename1.dat> <filename2.dat>" % sys.argv[0]
#     print "Example: %s ../seventh-cwnd-count.dat" % sys.argv[0]
#     sys.exit()

if args.merge:
    print "== 使用 merge 绘图模式"
else:
    print "== 使用 独立 绘图模式"

plt_handles = []
for this_file in args.filenames: # support multiple file
    if not args.merge:
        plt.clf() # 清除上一次绘图
    arr = np.genfromtxt(this_file)
    print ("读入了数据文件 %s" % this_file)
    this_handle, = plt.plot(arr[:,0], arr[:,1], label=this_file)
    if not args.merge:
        plt_handles = [this_handle]
    else:
        plt_handles += [this_handle]
    plt.title(this_file)
    plt.legend(handles=plt_handles)
    png_filename = "%s.%s" % (this_file, 'png')
    plt.savefig(png_filename) # 保存文件
    print ("生成了图形文件 %s" % png_filename)
    if len(sys.argv) == 2: # 如果仅有一个图表则显示, 否则只是批量生产png文件
        plt.show()

if args.merge: # merge模式下显示最后的图表
     plt.show()
