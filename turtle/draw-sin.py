# REF: https://zhuanlan.zhihu.com/p/31202953
# 绘制正弦曲线

import turtle  
import math  

window=turtle.Screen() #creat a screen  
pen=turtle.Turtle()  

pen.pu()
pen.setx(-300)
pen.sety(100*math.sin(-300/40))
pen.pd()

for i in range(-300,300):
    pen.setx(i)
    pen.sety(100*math.sin(i/40))
