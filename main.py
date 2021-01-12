# owen moogk
# ai flappy dino
# jan 1 2020

# imports
import pygame, random, os, time, sys, pickle
from random import randint
from pygame import mixer

# pygame settings
windowWidth = 900
windowHeight = 600
dinoHeight = 60
dinoWidth = 60
backgroundColor = (200,200,200)

# game settings
gameSpeed = 30
gravity = 0.8
jumpPower = 15
cactusHeight = 75
cactusWidth = 50
dinoX = 100
cactusSpeed = 10

# init
clock = pygame.time.Clock()
mixer.init()

# assets
cactusImg = pygame.transform.scale(pygame.image.load(os.path.join("assets","cactus.png")), (cactusWidth, cactusHeight))
dinoImg = pygame.transform.scale(pygame.image.load(os.path.join("assets","dino.png")), (dinoWidth, dinoHeight))
baseImg = pygame.image.load(os.path.join("assets","base.png"))
jumpSound = mixer.Sound("assets/jump.wav")
jumpSound.set_volume(0.05)

# fonts
pygame.font.init()
font = pygame.font.SysFont("comicsans", 50)

# display
screen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Dino Game')

# dino class
class dino:
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

# cactus class
class cactus:
    def __init__(self, y,x):
        self.y = y
        self.x = x

def getInputs():
    # looping thru events
    events = pygame.event.get()
    running = True
    for event in events:
        # if x button pressed stop just break out of these loops
        if event.type == pygame.QUIT:
            running = False
        # if key is pressed
        if event.type == pygame.KEYDOWN:
            # if space is pressed
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if d1.y >= windowHeight - dinoHeight:
                    d1.jump()
    return(running)

def restart(started):
    global d1, cactuss, died, score, highScore
    d1 = dino(dinoX,windowHeight-dinoHeight)
    cactuss = []
    cactuss.append(cactus(windowHeight - cactusHeight,windowWidth))
    died = True
    score = 0
    if started == False:
        if score > highScore:
            highScore = score
            pickle.dump(highScore, open("highscore.dat", "wb"))
    else:
        highScore = pickle.load(open("highscore.dat", "rb"))
        started = True

running = True
started = True

restart(started)

# main running loop
while running:

    if died == False:
        restart(started)
    
    # background
    pygame.draw.rect(screen, backgroundColor, (0,0,windowWidth, windowHeight))

    running = getInputs() # if return is false then user wants to quit; end while loop
    d1.move()

    # y collision detection
    if d1.y < 0:
        died = False
    if d1.y > windowHeight - dinoHeight:
        d1.y = windowHeight - dinoHeight

    # if the forwardmost cactus is off screen then delete
    if cactuss[len(cactuss)-1].x < windowWidth - 400:
        cactuss.append(cactus(windowHeight - cactusHeight, windowWidth))

    # loop thru cactuss
    for i in cactuss:

        # move cactuss
        i.x -= cactusSpeed

        # collision detection
        if i.x < d1.x + dinoWidth and i.x + cactusWidth > d1.x: # checking if the cactus x overlaps with the dino x
            if i.y < d1.y + dinoHeight:
                died = False
        
        # blit images
        screen.blit(cactusImg,(i.x,i.y))

        # when off screen delete
        if i.x < 0 - cactusWidth:
            cactuss.remove(cactuss[0])

    # score onto screen
    score_label = font.render("Score: " + str(score),1,(255,255,255))
    screen.blit(score_label, (10, 10))
    highScoreLabel = font.render("High Score: "+str(highScore),1,(255,255,255))
    screen.blit(highScoreLabel, (10, 50))

    # dino onto screen
    screen.blit(dinoImg,(d1.x,d1.y))
    # score
    score += 1

    # final update to the screen
    clock.tick(gameSpeed)
    pygame.display.update()