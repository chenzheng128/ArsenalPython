#coding:utf-8
#PythonDraw.py
import turtle
turtle.setup(600, 500, 200, 300)  # 绘图窗体 设置窗口大小 (width=200, height=200, startx=0, starty=0)
turtle.penup()
turtle.fd(-250)   # 相对于中心绝对坐标系 (0, 0) fd 向前 , bk 后退 , circle 画圆
turtle.pendown()
turtle.pensize(25)
turtle.pencolor("purple")  # a Tk color specification string, such as "red" or "yellow", magenta cyan blue black
turtle.seth(-40)  # 调整绝对角度
turtle.right(10)  # 调整相对角度
for i in range(4):
    turtle.circle(40, 80)
    turtle.circle(-40, 80)
turtle.circle(40, 80/2)
turtle.fd(40)
turtle.circle(16, 180)
turtle.fd(40 * 2/3)
turtle.done()