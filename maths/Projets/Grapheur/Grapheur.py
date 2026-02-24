import turtle
import math
turtle.setworldcoordinates(-300, -300, 300, 300)
turtle.speed(0)
turtle.showturtle()
turtle.bgcolor("black")
turtle.title("Grapheur basique | Timothé")
turtle.pensize(3)
turtle.goto(0, 0)
turtle.penup()
turtle.color("red")
turtle.goto(-300, 0) #nous n'utiliserons pas cette fonction pour le tracé graphique (que des turle.forward)
turtle.pendown()
turtle.goto(300, 0)
turtle.penup()
turtle.goto(0, -300) #nous n'utiliserons pas cette fonction pour le tracé graphique (que des turle.forward)
turtle.pendown()
turtle.goto(0, 300) #nous n'utiliserons pas cette fonction pour le tracé graphique (que des turle.forward)
turtle.penup()
turtle.goto(-300,0)
def goto(x, y, oldy):
    turtle.setheading(0)
    AB = (100 + abs(oldy - y)**2)**0.5
    Angle = math.atan(abs(oldy - y) / 10)

    if y > oldy:
        turtle.left(math.degrees(Angle))
    else:
        turtle.right(math.degrees(Angle))
    turtle.forward(AB)

def Grapheur() :
    a=str(input("Entrez une fonction"))
    def f(x):
        return eval(a, {"__builtins__": None}, {"x": x, "math": math, **math.__dict__})
    x=-300
    y=float(f(x))
    oldy=y
    
    #Il faut vérifier ymax et ymin pour l'échelle (approximativement)
    ymax=0
    ymin=0
    yabs=0
    while x !=300 :
        x = x+10 
        y=f(x)
        if ymin > y:
            ymin=y
        elif ymax < y: 
            ymax=y
    print ("ymax est probablement ", ymax, " et ymin est probablement", ymin)
    if abs(ymin) > abs(ymax):
        yabs=ymin
    else :
        yabs=ymax
    #Sur un segment de 300 unités, yabs doit rentrer (tout pile + 10 pour ne pas frôler. On a donc une équation ymax*echelle=300-10
    echelle=290/ymax
    
    x=-300
    y=f(x)
    turtle.pendown()
    turtle.color("blue")
    turtle.penup()
    turtle.goto(x, y * echelle)
    turtle.pendown()
    while x != 300:
        oldy=y
        x=x+10
        y=f(x)
        goto(x, y * echelle, oldy * echelle)
Grapheur()
turtle.done()