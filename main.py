import pygame, os, time, sys, keyboard
from random import uniform, randint
from settings import *
from objects.dino import *
from objects.cactus import *
from objects.bird import *

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

def restart():
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
    if score < 100:
        enemies.append(Cactus(windowHeight - cactusHeight, windowWidth))
    else:
        # chance of spawning a bird
        randomNum = randint(0,2)
        if randomNum == 0:
            birdY = randint(1,3)
            if birdY == 3:
                enemies.append(Bird(windowHeight - birdY * birdHeight - 60, windowWidth))
            else:
                enemies.append(Bird(windowHeight - birdY * birdHeight - 5, windowWidth))
        else:
            enemies.append(Cactus(windowHeight - cactusHeight, windowWidth))
    if score > 5000:
        chosenTimeDelay = uniform(0.6,0.85)
    elif score > 2500:
        chosenTimeDelay = uniform(0.7,1)
    else:
        chosenTimeDelay = uniform(0.8,1.2)

cactusSpeed = cactusBaseSpeed
restart()

# main running loop
while True:
    # changing the cactus speed based on score
    cactusSpeed = cactusBaseSpeed + (cactusBaseSpeed * (score / 2000))
    if died == True:
        restart()
    if getInputs() == False:
        quit()

    d1.move()

    timeSinceLastCactus = time.time() - lastCactusTime
    if timeSinceLastCactus >= chosenTimeDelay:
        appendEnemy()
        lastCactusTime = time.time()

    for enemy in enemies:
        enemy.move(cactusSpeed)
        died = enemy.collision(d1)
        if died:
            break
        if enemy.x < 0 - 100:
            enemies.remove(enemies[0])

    score += 1
    renderScreen(d1, enemies)
    clock.tick(gameSpeed)
    pygame.display.update()