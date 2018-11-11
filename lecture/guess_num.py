#conding:utf-8
# filename: guess_num.py

import random

print ("游戏结束，您要猜的数字是 {}".format(random.randrange(1,10)))


level = 3

def chooselevel():
	# global level2
	print("选择难度为：", level)

chooselevel()
