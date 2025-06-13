import turtle
import math

# --- Paramètres du quadrillage ---
step = 50  # distance entre les lignes du quadrillage
size = 500  # taille du plan

# --- Initialisation de la fenêtre ---
turtle.setup(size + 100, size + 100)
turtle.speed(0)
turtle.hideturtle()
turtle.bgcolor("white")
turtle.title("Grapheur - Sans biblis")

# --- Quadrillage ---
def draw_grid():
    turtle.pencolor("lightgray")
    for x in range(-size // 2, size // 2 + 1, step):
        turtle.penup()
        turtle.goto(x, -size // 2)
        turtle.pendown()
        turtle.goto(x, size // 2)
    for y in range(-size // 2, size // 2 + 1, step):
        turtle.penup()
        turtle.goto(-size // 2, y)
        turtle.pendown()
        turtle.goto(size // 2, y)

    # Axes
    turtle.pencolor("black")
    turtle.penup()
    turtle.goto(-size // 2, 0)
    turtle.pendown()
    turtle.goto(size // 2, 0)
    turtle.penup()
    turtle.goto(0, -size // 2)
    turtle.pendown()
    turtle.goto(0, size // 2)

# --- Coordonnées de départ ---
X0, Y0 = 0, 0  # touche l'axe des ordonnées et l'axe des abcisses (donc en gors axe de symétrie)
draw_grid()
def Fonction(x):
    return 2 * x + 5
    
xmin=-25
xmax=25
xa=xmin
ya=Fonction(xa)
turtle.goto(xa, ya)

def avancer_et_orienter(xb, yb, xa, ya):
    AB=math.sqrt((xa-xb)**2+(ya-yb)**2)
    Orientation=math.acos((xb-xa)/AB)
    angle_degres = math.degrees(Orientation)  # Conversion en degrés (fois pi/180)
    if yb > ya:
        Orientation=360-Orientation #En théorie, on pourrait juste mettre un - mais je préfère les angles positifs
    turtle.setheading(Orientation)
    turtle.pendown()     
    turtle.forward(AB)   
    turtle.penup()  
    turtle.setheading(90)

Compteur=math.sqrt((xmin)**2)+math.sqrt((xmax)**2)
Compt=0
while Compt!=Compteur:
    xb=xa+1/10
    yb=Fonction(xb)
    avancer_et_orienter(xb, yb, xa, ya)
    xa=xb
    ya=yb







    
    
    
turtle.done()
