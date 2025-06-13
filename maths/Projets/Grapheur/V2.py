import turtle
import math
import random

# --- Paramètres initiaux ---
step = 1.0               # largeur d'une grille en unités mathématiques
scale = 50.0             # pixels par unité mathématique
origin_x = 0.0           # coordonnées de l'origine (centre de l'écran) en unités
origin_y = 0.0
dx = 0.1                 # pas pour l'échantillonnage

# Liste des fonctions à tracer
fonctions = []

def ajouter_fonction():
    nom = input("Nom de la fonction (ex: f, g, h) : ")
    expr = input(f"{nom}(x) = ")
    couleur = input("Couleur (red, blue, green...) [laisser vide pour aléatoire] : ")
    if couleur.strip() == "":
        couleur = random.choice(["red", "blue", "green", "orange", "purple", "brown", "black"])
    fonctions.append({"nom": nom, "expr": expr, "couleur": couleur})

# Entrée des fonctions
print("Entrez les fonctions à tracer (laisser vide pour arrêter)")
while True:
    ajouter = input("Ajouter une fonction ? (o/n) : ").strip().lower()
    if ajouter == 'o':
        ajouter_fonction()
    else:
        break

# --- Initialisation de la fenêtre ---
screen = turtle.Screen()
screen.setup(800, 800)
screen.title("Grapheur infini avec zoom et pan et fonctions multiples")

# Deux tortues : une pour la grille, une pour les fonctions
grid_t = turtle.Turtle()
grid_t.hideturtle()
grid_t.speed(0)
func_t = turtle.Turtle()
func_t.hideturtle()
func_t.speed(0)

# --- Conversion coordonnées monde -> écran ---
def world_to_screen(x, y):
    sx = (x - origin_x) * scale
    sy = (y - origin_y) * scale
    return sx, sy

# --- Frange utilitaire ---
def frange(start, stop, step):
    x = start
    while x <= stop:
        yield x
        x += step

# --- Dessin du quadrillage infini ---
def draw_grid(left, right, bottom, top):
    grid_t.clear()
    width, height = screen.window_width(), screen.window_height()
    # lignes verticales
    start_x = math.floor(left/step) * step
    end_x = math.ceil(right/step) * step
    grid_t.pencolor("lightgray")
    for gx in frange(start_x, end_x, step):
        sx, _ = world_to_screen(gx, 0)
        grid_t.penup(); grid_t.goto(sx, -height/2); grid_t.pendown(); grid_t.goto(sx, height/2)
    # lignes horizontales
    start_y = math.floor(bottom/step) * step
    end_y = math.ceil(top/step) * step
    for gy in frange(start_y, end_y, step):
        _, sy = world_to_screen(0, gy)
        grid_t.penup(); grid_t.goto(-width/2, sy); grid_t.pendown(); grid_t.goto(width/2, sy)
    # axes
    grid_t.pencolor("black")
    # axe Y
    sx0, sy0 = world_to_screen(0, bottom)
    sx1, sy1 = world_to_screen(0, top)
    grid_t.penup(); grid_t.goto(sx0, sy0); grid_t.pendown(); grid_t.goto(sx1, sy1)
    # axe X
    sx0, sy0 = world_to_screen(left, 0)
    sx1, sy1 = world_to_screen(right, 0)
    grid_t.penup(); grid_t.goto(sx0, sy0); grid_t.pendown(); grid_t.goto(sx1, sy1)

# --- Dessin de toutes les fonctions ---
def draw_all_functions(left, right):
    func_t.clear()
    for f in fonctions:
        expr = f["expr"]
        color = f["couleur"]
        func_t.pencolor(color)
        first = True
        for x in frange(left, right, dx):
            try:
                y = eval(expr, {"x": x, "math": math})
                sx, sy = world_to_screen(x, y)
                if first:
                    func_t.penup(); func_t.goto(sx, sy); func_t.pendown()
                    first = False
                else:
                    func_t.goto(sx, sy)
            except:
                func_t.penup()
                first = True

# --- Recalcul des limites et redraw complet ---
def redraw():
    screen.tracer(False)
    width, height = screen.window_width(), screen.window_height()
    left   = origin_x - (width/2)/scale
    right  = origin_x + (width/2)/scale
    bottom = origin_y - (height/2)/scale
    top    = origin_y + (height/2)/scale
    draw_grid(left, right, bottom, top)
    draw_all_functions(left, right)
    screen.tracer(True)

# --- Handlers clavier ---
def zoom_in():
    global scale
    scale *= 1.1
    redraw()

def zoom_out():
    global scale
    scale /= 1.1
    redraw()

def pan_left():
    global origin_x
    origin_x -= (20 / scale)
    redraw()

def pan_right():
    global origin_x
    origin_x += (20 / scale)
    redraw()

def pan_up():
    global origin_y
    origin_y += (20 / scale)
    redraw()

def pan_down():
    global origin_y
    origin_y -= (20 / scale)
    redraw()

# --- Bindings ---
screen.listen()
screen.onkey(zoom_in, "+")
screen.onkey(zoom_out, "-")
screen.onkey(pan_left, "Left")
screen.onkey(pan_right, "Right")
screen.onkey(pan_up, "Up")
screen.onkey(pan_down, "Down")

# Lancement initial
redraw()
screen.mainloop()
