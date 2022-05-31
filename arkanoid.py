"""
https://new.pythonforengineers.com/blog/your-first-game-in-python-in-less-than-30-minutes/
"""
import time

import pgzrun
import random


TITLE = "Crescio's Arkanoid"
WIDTH = 800
HEIGHT = 500

paddle = Actor("paddleblue.png")
paddle.x = 120
paddle.y = 420
paddle.width = 55


def ini_ball():
    ball.x = random.randint(1, WIDTH)
    ball.y = random.randint(250, 350)

ball = Actor("ballblue.png")
ini_ball()
ball_x_speed = 2
ball_y_speed = 2

bars_list = []


class GameOverException(Exception):
    def __init__(self):
        screen.draw.text("GAME OVER", (300, 300), color="green")

class Game:
    def __init__(self):
        self.lives = 3
        self.points = 0
        self.speed = 1

    def add_points(self,points):
        self.points = self.points + points

    def draw(self):
        screen.draw.text(str(self.points), (50, 30), color="orange")
        screen.draw.text(str(self.lives), (700, 30), color="green")

    def subs_lives(self):
        self.lives = self.lives - 1


game = Game()

def draw():
    screen.blit("background.png", (0, 0))
    paddle.draw()
    ball.draw()
    for bar in bars_list:
        bar.draw()
    game.draw()

def place_bars(x,y,image):
    bar_x = x
    bar_y = y
    for i in range(8):
        bar = Actor(image)
        bar.x = bar_x
        bar.y = bar_y
        bar_x += 70
        bar.point = 1
        bars_list.append(bar)

def update():
    global ball_x_speed, ball_y_speed

    update_paddle()
    update_ball()
    update_bars()
    update_game()

def update_paddle():
    global ball_x_speed, ball_y_speed
    if keyboard.left and paddle.x >= paddle.width:
        paddle.x = paddle.x - 5
    if keyboard.right and paddle.x <= WIDTH - paddle.width:
        paddle.x = paddle.x + 5

def update_bars():
    global ball_x_speed, ball_y_speed
    for bar in bars_list:
        if ball.colliderect(bar):
            music.play_once("beep-07a")
            game.add_points(bar.point)
            bars_list.remove(bar)
            collision_x = []
            collision_x.append(ball.collidepoint(bar.midleft))
            collision_x.append(ball.collidepoint(bar.midright))
            if True in collision_x:
                ball_x_speed *= -1  ##Si colisiona en la izq o derecha de una bar tiene que cambiar x
            else:
                ball_y_speed *= -1

def update_ball():
    global ball_x_speed, ball_y_speed
    ball.x -= ball_x_speed
    ball.y -= ball_y_speed
    if (ball.x >= WIDTH) or (ball.x <= 0):
        ball_x_speed *= -1
    if (ball.y >= HEIGHT):  ### Si se va para abajo. Quedé acá
        game.subs_lives()
        ini_ball()
        music.play_once("beep-10")
        ball_y_speed *= -1
        time.sleep(1)

    if (ball.y <= 0):
        ball_y_speed *= -1
    if paddle.colliderect(ball):
        ball_y_speed *= -1

def update_game():
    if game.lives <= 0:
        raise GameOverException()

coloured_box_list = ["element_blue_rectangle_glossy.png", "element_green_rectangle_glossy.png", "element_red_rectangle_glossy.png"]
x = 120
y = 100
for coloured_box in coloured_box_list:
    place_bars(x, y, coloured_box)
    y += 50

pgzrun.go()