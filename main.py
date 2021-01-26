# owen moogk
# ai dino game

import pygame, random, os, time, sys, pickle, keyboard
from random import randint
from pygame import mixer

# pygame settings
windowWidth = 900
windowHeight = 600
dinoHeight = 60
dinoWidth = 60
backgroundColor = (200,200,200)

# game settings
gameSpeed = 65
gravity = 1.5
jumpPower = 22.5
cactusHeight = 50
cactusWidth = 50
dinoX = 100
cactusSpeed = 10
scoreColor = (0,0,0)

# init
clock = pygame.time.Clock()
mixer.init()

# assets
cactusImg = pygame.transform.scale(pygame.image.load(os.path.join("assets","cactus.png")), (cactusWidth, cactusHeight))
dinoImg = pygame.transform.scale(pygame.image.load(os.path.join("assets","dino.png")), (dinoWidth, dinoHeight))
baseImg = pygame.image.load(os.path.join("assets","base.png"))
jumpSound = mixer.Sound("assets/jump.wav")
jumpSound.set_volume(0.01)

# fonts
pygame.font.init()
font = pygame.font.SysFont("comicsans", 50)

# display
screen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Dino Game')

class Dino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ySpeed = 0
    def jump(self):
        self.ySpeed = 0-jumpPower
        jumpSound.play()
    def move(self):  
        self.ySpeed += gravity
        self.y += self.ySpeed
        if self.y > windowHeight - dinoHeight:
            self.y = windowHeight - dinoHeight

class Cactus:
    def __init__(self, y, x):
        self.y = y
        self.x = x
    def move(self):
        self.x -= cactusSpeed
    def collision(self, dino):
        collided = False
        if self.x < dino.x + dinoWidth and self.x + cactusWidth > dino.x: # checking if the cactus x overlaps with the dino x
            if self.y < dino.y + dinoHeight:
                collided = True
        return(collided)

class Bird():
    def __init__(self, y,x):
        self.y = y
        self.x = x

def getInputs():
    events = pygame.event.get()
    for event in events:
        # if x button pressed stop just break out of these loops
        if event.type == pygame.QUIT:
            quit()      
        if keyboard.is_pressed('space'):
            if d1.y >= windowHeight - dinoHeight:
                d1.jump()

def restart(started):
    global d1, cacti, died, score, highScore
    d1 = Dino(dinoX,windowHeight-dinoHeight)
    cacti = []
    cacti.append(Cactus(windowHeight - cactusHeight,windowWidth))
    died = False
    score = 0
    if started == False:
        if score > highScore:
            highScore = score
            pickle.dump(highScore, open("highscore.dat", "wb"))
    else:
        highScore = pickle.load(open("highscore.dat", "rb"))
        started = True

def renderScreen(dino, cacti):
    pygame.draw.rect(screen, backgroundColor, (0,0,windowWidth, windowHeight))
    screen.blit(dinoImg,(dino.x,dino.y))
    for cactus in cacti:
        screen.blit(cactusImg,(cactus.x,cactus.y))

    # scores
    score_label = font.render("Score: " + str(score),1,(scoreColor))
    screen.blit(score_label, (10, 10))
    highScoreLabel = font.render("High Score: "+str(highScore),1,(scoreColor))
    screen.blit(highScoreLabel, (10, 50))

started = True
restart(started)

# main running loop
while True:
    if died == True:
        restart(started)
    if getInputs() == False:
        quit()
    d1.move()

    # if the forward most cactus is off screen then delete
    if cacti[len(cacti)-1].x < windowWidth - 400:
        cacti.append(Cactus(windowHeight - cactusHeight, windowWidth))

    for cactus in cacti:
        cactus.move()
        died = cactus.collision(d1)
        if died:
            break
        if cactus.x < 0 - cactusWidth:
            cacti.remove(cacti[0])

    score += 1
    renderScreen(d1, cacti)
    clock.tick(gameSpeed)
    pygame.display.update()