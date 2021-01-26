# owen moogk
# ai dino game

import pygame, random, os, time, sys, pickle, keyboard, time
from random import uniform
from pygame import mixer

# pygame settings
windowWidth = 1400
windowHeight = 600
dinoHeight = 60
dinoWidth = 60
backgroundColor = (200,200,200)

# game settings
gameSpeed = 60 
gravity = 1.5
jumpPower = 22.5
cactusHeight = 70
cactusWidth = 40
dinoX = 100
cactusBaseSpeed = 13
cactusSpeed = cactusBaseSpeed
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
        if d1.y >= windowHeight - dinoHeight:
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
    keys = pygame.key.get_pressed()  # checking pressed keys
    if keys[pygame.K_SPACE]:             
        d1.jump()

def restart(started):
    global d1, cacti, died, score, lastCactusTime, chosenTimeDelay
    d1 = Dino(dinoX,windowHeight-dinoHeight)
    cacti = []
    cacti.append(Cactus(windowHeight - cactusHeight,windowWidth))
    died = False
    score = 0
    chosenTimeDelay = 1
    lastCactusTime = time.time()

def renderScreen(dino, cacti):
    pygame.draw.rect(screen, backgroundColor, (0,0,windowWidth, windowHeight))
    screen.blit(dinoImg,(dino.x,dino.y))
    for cactus in cacti:
        screen.blit(cactusImg,(cactus.x,cactus.y))
    # score
    score_label = font.render("Score: " + str(score),1,(scoreColor))
    screen.blit(score_label, (10, 10))

def appendCactus():
    global chosenTimeDelay
    cacti.append(Cactus(windowHeight - cactusHeight, windowWidth))
    chosenTimeDelay = random.uniform(0.8,1.2)

started = True
restart(started)

# main running loop
while True:

    cactusSpeed = cactusBaseSpeed + (cactusBaseSpeed * (score / 2000))
    print(cactusSpeed)

    if died == True:
        restart(started)
    if getInputs() == False:
        quit()
    d1.move()

    timeSinceLastCactus = time.time() - lastCactusTime
    if timeSinceLastCactus >= chosenTimeDelay:
        appendCactus()
        lastCactusTime = time.time()

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