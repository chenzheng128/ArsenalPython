#REF: cheatsheet2.pdf

import turtle
import random
random.seed()
turtle.speed(10)
turtle.resizemode('auto')

myColourList = ['red', 'black', 'orange', 'blue', 'purple']

myShapeList = ['turtle', 'arrow', 'square', 'circle', 'triangle', 'classic']

def makeStamp():
    turtle.setheading(random.randint(1, 360))
    turtle.pensize(random.randint(1, 7))
    turtle.color(random.choice(myColourList))
    turtle.shape(random.choice(myShapeList))
    turtle.stamp()

for i in range(200):
    makeStamp()
    # turtle.setheading(90)
    turtle.penup()

    turtle.fd(random.randint(50,100))
    if (turtle.pos()[0]) > 400 or (turtle.pos()[0]) < -400:
    	turtle.home()
    turtle.pendown()

turtle.done()