# REF: ttps://docs.python.org/3.7/library/turtle.html#turtle.onkey


from turtle import *
import turtle
import random

myColourList = ['red', 'black', 'orange', 'blue', 'purple']

myShapeList = ['turtle', 'arrow', 'square', 'circle', 'triangle', 'classic']

def makeStamp(x, y):
    turtle.hideturtle()
    turtle.setheading(random.randint(1, 360))
    turtle.pensize(random.randint(100, 100))
    turtle.color(random.choice(myColourList))
    turtle.shape(random.choice(myShapeList))

    turtle.penup()
    
    turtle.goto(x, y)
    
    turtle.pendown()
    
    turtle.stamp()
    turtle.showturtle()

def f():
    fd(50)
    lt(60)

onscreenclick(makeStamp) # 鼠标绑定
onkey(f, "Up") # 键盘绑定
listen()  # set focus on screen / 不加这一句 onkey 不起作用， 但是  onclick 可以 

done()    # 在 命令行（不马上退出） 或 ipython （能获取焦点)  中执行需要

"""
mainloop()  # 在命令行中执行 
Starts event loop - calling Tkinter's mainloop function.
Must be last statement in a turtle graphics program.
"""


"""
onclick / onrelease 不起作用， 待调试

from turtle import *
class MyTurtle(Turtle):
    def glow(self,x,y):
        self.fillcolor("red")
    def unglow(self,x,y):
        self.fillcolor("")

turtle = MyTurtle()
turtle.onclick(turtle.glow)     # clicking on turtle turns fillcolor red,
turtle.onrelease(turtle.unglow) # releasing turns it to transparent.
"""