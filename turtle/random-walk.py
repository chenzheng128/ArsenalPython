# REF: http://interactivepython.org/runestone/static/CS152f17/MoreAboutIteration/RandomlyWalkingTurtles.html

import random
import turtle


def isInScreen(w, t):
    if random.random() > 0.1:
        return True
    else:
        return False

def isInScreen(w,t):
    leftBound = - w.window_width() / 2
    rightBound = w.window_width() / 2
    topBound = w.window_height() / 2
    bottomBound = -w.window_height() / 2

    turtleX = t.xcor()
    turtleY = t.ycor()

    stillIn = True
    if turtleX > rightBound or turtleX < leftBound:
        stillIn = False
    if turtleY > topBound or turtleY < bottomBound:
        stillIn = False

    return stillIn


t = turtle.Turtle()
wn = turtle.Screen()

t.shape('turtle')
while True:
    if not isInScreen(wn, t):
        t.penup()
        t.home()
        t.pendown()
    coin = random.randrange(0, 2)
    if coin == 0:              # heads
        t.left(90)
    else:                      # tails
        t.right(90)

    t.forward(50)

wn.exitonclick()
