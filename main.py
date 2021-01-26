# owen moogk
# ai dino game

import pygame, random, os, time, sys, pickle, keyboard, time
from random import uniform, randint
from pygame import mixer

# pygame settings
windowWidth = 1400
windowHeight = 600
# png files ===> 47,30,44,60
dinoDefaultHeight = 70
dinoDuckHeight = 45
dinoDefaultWidth = 66
dinoDuckWidth = 90
backgroundColor = (50,50,50)

# game settings
gameSpeed = 60 
gravity = 1.5
jumpPower = 25
# 70,40
cactusHeight = 91
cactusWidth = 52
dinoX = 100
cactusBaseSpeed = 13
cactusSpeed = cactusBaseSpeed
scoreColor = (255,255,255)
# 30, 40
birdHeight = 46
birdWidth = 62

# init
clock = pygame.time.Clock()
mixer.init()

# assets
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
        self.height = dinoDefaultHeight
        self.width = dinoDefaultWidth
        self.ySpeed = 0
        self.isDucked = False
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("assets","dino.png")), (self.width, self.height))
    def jump(self):
        if self.y >= windowHeight - self.height:
            self.ySpeed = 0-jumpPower
            jumpSound.play()
    def touchingGround(self):
        if self.y >= windowHeight - self.height:
            return(True)
    def move(self): 
        self.ySpeed += gravity
        self.y += self.ySpeed
        if self.touchingGround():
            self.y = windowHeight - self.height
    def duck(self):
        if not self.touchingGround():
            self.ySpeed += 2
        elif self.isDucked == False:
            self.isDucked = True
            self.height = dinoDuckHeight
            self.width = dinoDuckWidth
            self.img = pygame.transform.scale(pygame.image.load(os.path.join("assets","dino-duck.png")), (self.width, self.height))
    def unduck(self):
        if self.isDucked:
            self.isDucked = False
            self.height = dinoDefaultHeight
            self.width = dinoDefaultWidth 
            self.img = pygame.transform.scale(pygame.image.load(os.path.join("assets","dino.png")), (self.width, self.height))

class Cactus:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("assets","cactus.png")), (cactusWidth, cactusHeight))
    def move(self):
        self.x -= cactusSpeed
    def collision(self, dino):
        collided = False
        if self.x < dino.x + dino.width and self.x + cactusWidth > dino.x: # checking if the cactus x overlaps with the dino x
            if self.y < dino.y + dino.height:
                collided = True
        return(collided)

class Bird():
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("assets","bird.png")), (birdWidth, birdHeight))
    def move(self):
        self.x -= cactusSpeed
    def collision(self, dino):
        collided = False
        if self.x < dino.x + dino.width and self.x + birdWidth > dino.x: # checking if the bird x overlaps with the dino x
            if self.y < dino.y + dino.height and self.y + birdHeight > dino.y:
                collided = True
        return(collided)

def getInputs():
    events = pygame.event.get()
    for event in events:
        # if x button pressed stop just break out of these loops
        if event.type == pygame.QUIT:
            quit()
    keys = pygame.key.get_pressed()  # checking pressed keys
    if keys[pygame.K_DOWN]:
        d1.duck()
    elif keys[pygame.K_SPACE] or keys[pygame.K_UP]:             
        d1.jump()
    else:
        d1.unduck()

def restart(started):
    global d1, enemies, died, score, lastCactusTime, chosenTimeDelay
    d1 = Dino(dinoX,windowHeight-dinoDefaultHeight)
    enemies = []
    enemies.append(Cactus(windowHeight - cactusHeight,windowWidth))
    died = False
    score = 0
    chosenTimeDelay = 1
    lastCactusTime = time.time()

def renderScreen(dino, enemies):
    pygame.draw.rect(screen, backgroundColor, (0,0,windowWidth, windowHeight))
    screen.blit(dino.img,(dino.x,dino.y))
    for enemy in enemies:
        screen.blit(enemy.img,(enemy.x,enemy.y))
    # score
    score_label = font.render("Score: " + str(score),1,(scoreColor))
    screen.blit(score_label, (10, 10))

def appendEnemy():
    global chosenTimeDelay
    if score < 1000:
        enemies.append(Cactus(windowHeight - cactusHeight, windowWidth))
    else:
        # chance of spawning a bird
        randomNum = randint(0,5)
        if randomNum == 0:
            birdY = randint(1,3)
            if birdY == 3:
                enemies.append(Bird(windowHeight - birdY * birdHeight - 55, windowWidth))
            else:
                enemies.append(Bird(windowHeight - birdY * birdHeight - 5, windowWidth))
        else:
            enemies.append(Cactus(windowHeight - cactusHeight, windowWidth))
    if score > 5000:
        chosenTimeDelay = random.uniform(0.6,0.85)
    elif score > 2500:
        chosenTimeDelay = random.uniform(0.7,1)
    else:
        chosenTimeDelay = random.uniform(0.8,1.2)

started = True
restart(started)

# main running loop
while True:
    # changing the cactus speed based on score
    cactusSpeed = cactusBaseSpeed + (cactusBaseSpeed * (score / 2000))
    if died == True:
        restart(started)
    if getInputs() == False:
        quit()

    d1.move()

    timeSinceLastCactus = time.time() - lastCactusTime
    if timeSinceLastCactus >= chosenTimeDelay:
        appendEnemy()
        lastCactusTime = time.time()

    for enemy in enemies:
        enemy.move()
        died = enemy.collision(d1)
        if died:
            break
        if enemy.x < 0 - 100:
            enemies.remove(enemies[0])

    score += 1
    renderScreen(d1, enemies)
    clock.tick(gameSpeed)
    pygame.display.update()