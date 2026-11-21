from pygame import *
from random import randint
from time import time as timer  # Importar la función temporizadora para que el intérprete no necesite buscar esta función en el módulo time de pygame, necesitamos darle un nombre diferente

# cargar las funciones font por separado
font.init()
font1 = font.Font(None, 80)
win = font1.render("¡GANASTE!", True, (255, 255, 255))
lose = font1.render("¡PERDISTE!", True, (180, 0, 0))

font2 = font.Font(None, 36)

# música de fondo
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

# necesitamos las siguientes imágenes:
img_back = "galaxy.jpg"  # Fondo de juego
img_bullet = "bullet.png"  # bala
img_hero = "rocket.png"  # héroe
img_enemy = "ufo.png"  # enemigo
img_ast = "asteroid.png"  # asteroide

score = 0  # naves destruidas
goal = 20  # la cantidad de naves que necesitan ser destruidas para ganar
lost = 0  # naves falladas
max_lost = 10  # pierdes si fallas tantas naves
life = 3  # puntos de vida


# clase padre para los otros objetos
class GameSprite(sprite.Sprite):
    # constructor de clase
    def __init__(
        self, player_image, player_x, player_y, size_x, size_y, player_speed
    ):
        # Llamada para el constructor de la clase (Sprite):
        sprite.Sprite.__init__(self)
        # cada objeto debe almacenar la propiedad image
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y)
        )
        self.speed = player_speed
        # cada objeto debe tener la propiedad rect – el rectángulo en el que se encuentra
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # método de dibujo del personaje en la ventana
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# clase principal del jugador
class Player(GameSprite):
    # método para controlar el objeto con las flechas
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    # método para “disparar” (usar la posición del jugador para crear una bala)
    def fire(self):
        bullet = Bullet(
            img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15
        )
        bullets.add(bullet)


# clase del objeto enemigo
class Enemy(GameSprite):
    # movimiento del enemigo
    def update(self):
        self.rect.y += self.speed
        global lost
        # desaparece al alcanzar el borde de la pantalla
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1


# clase del objeto bullet
class Bullet(GameSprite):
    # movimiento del enemigo
    def update(self):
        self.rect.y += self.speed
        # clase del objeto bullet
        if self.rect.y < 0:
            self.kill()


# Crear una ventana pequeña
win_width = 700
win_height = 500
display.set_caption("Tirador")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# crear objetos
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

# Crear un grupo de objetos enemigos
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(
        img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5)
    )
    monsters.add(monster)

# crear un grupo de objetos asteroides ()
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(
        img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7)
    )
    asteroids.add(asteroid)

bullets = sprite.Group()

# la variable “juego terminado”: cuando sea True, los objetos dejan de funcionar en el ciclo principal
finish = False

# Ciclo de juego principal:
run = True  # la bandera es reiniciada por el botón de cerrar ventana

rel_time = False  # bandera a cargo del reinicio

num_fire = 0  # variable para contar disparos

while run:
    # Evento para presionar botón “Cerrar”
    for e in event.get():
        if e.type == QUIT:
            run = False
        # evento para presionar barra espaciadora – el objeto dispara
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                # comprueba cuántos disparos han sido disparados y si el recargo está en progreso
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 5 and rel_time == False:  # si el jugador hizo 5 disparos
                    last_time = timer()  # registra el tiempo cuando esto sucedió
                    rel_time = True  # establece la bandera de reinicio

    # el juego: acciones de los objetos, comprueba las reglas del juego, se vuelve a dibujar
    if not finish:
        # actualiza el fondo
        window.blit(background, (0, 0))

        # ejecuta los movimientos del objeto
        ship.update()
        monsters.update()
        asteroids.update()