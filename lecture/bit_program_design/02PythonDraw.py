#coding:utf-8
#PythonDraw.py
import turtle
turtle.setup(600, 500, 200, 300)  # 绘图窗体 设置窗口大小 (width=200, height=200, startx=0, starty=0)
turtle.penup()
turtle.fd(-100)   # 相对于中心绝对坐标系 (0, 0) fd 向前 , bk 后退 , circle 画圆
turtle.pendown()

# 雪花（多种颜色）绘图
turtle.pensize(10)	
for x in range(1): # 多重绘制
	colorlist=["black", "red", "yellow", "cyan", "purple", "green", "blue"]
	for c in colorlist:
		turtle.right(360/len(colorlist))  # 调整相对角度
		turtle.pencolor(c)
		turtle.fd(30)
		# turtle.circle(10, 180)
		turtle.bk(50)
	turtle.penup()
	turtle.left(45)
	turtle.fd(100)
	turtle.pendown()

exit 
# 原始蟒蛇（缩小尺寸） 绘图
turtle.pensize(20)	
turtle.pencolor("purple")  # a Tk color specification string, such as "red" or "yellow", magenta cyan blue black
turtle.seth(-40)  # 调整绝对角度

for i in range(4):
    turtle.circle(30, 60)
    turtle.circle(-30, 60)
turtle.circle(30, 60/2)
turtle.fd(30)
turtle.circle(12, 180)
turtle.fd(30 * 2/3)
turtle.done()