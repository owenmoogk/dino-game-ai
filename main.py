# owen moogk
# ai dino game

import pygame, random, os, time, sys, pickle, keyboard, time, neat
from random import uniform, randint
from pygame import mixer

# ai
gen = 0

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
        else:
            self.unduck()
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
        self.level = 0
    def move(self):
        self.x -= cactusSpeed
    def collision(self, dino):
        collided = False
        if self.x < dino.x + dino.width and self.x + cactusWidth > dino.x: # checking if the cactus x overlaps with the dino x
            if self.y < dino.y + dino.height:
                collided = True
        return(collided)

class Bird():
    def __init__(self, y, x, level):
        self.y = y
        self.x = x
        self.level = level
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("assets","bird.png")), (birdWidth, birdHeight))
    def move(self):
        self.x -= cactusSpeed
    def collision(self, dino):
        collided = False
        if self.x < dino.x + dino.width and self.x + birdWidth > dino.x: # checking if the bird x overlaps with the dino x
            if self.y < dino.y + dino.height and self.y + birdHeight > dino.y:
                collided = True
        return(collided)

def doClose():
    events = pygame.event.get()
    for event in events:
        # if x button pressed stop just break out of these loops
        if event.type == pygame.QUIT:
            quit()

def renderScreen(dinos, enemies):
    pygame.draw.rect(screen, backgroundColor, (0,0,windowWidth, windowHeight))
    for enemy in enemies:
        screen.blit(enemy.img,(enemy.x,enemy.y))
    for dino in dinos:
        screen.blit(dino.img,(dino.x,dino.y))
    # labels
    score_label = font.render("Score: " + str(score),1,(scoreColor))
    screen.blit(score_label, (10, 10))
    score_label = font.render("Gens: " + str(gen),1,(255,255,255))
    screen.blit(score_label, (10, 50))
    score_label = font.render("Alive: " + str(len(dinos)),1,(255,255,255))
    screen.blit(score_label, (10, 90))

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
                enemies.append(Bird(windowHeight - birdY * birdHeight - 55, windowWidth, birdY))
            else:
                enemies.append(Bird(windowHeight - birdY * birdHeight - 5, windowWidth, birdY))
        else:
            enemies.append(Cactus(windowHeight - cactusHeight, windowWidth))
    if score > 5000:
        chosenTimeDelay = random.uniform(0.6,0.85)
    elif score > 2500:
        chosenTimeDelay = random.uniform(0.7,1)
    else:
        chosenTimeDelay = random.uniform(0.8,1.2)

def eval_genomes(genomes, config):

    global gen, lastCactusTime, dinos, score, enemies
    enemies = []
    enemies.append(Cactus(windowHeight - cactusHeight,windowWidth))
    score = 0
    chosenTimeDelay = 1
    lastCactusTime = time.time()
 
    gen += 1

    nets = []
    dinos = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        # making a bird for every gene / neural network
        dinos.append(Dino(dinoX,windowHeight-dinoDefaultHeight))
        ge.append(genome)


    # main running loop
    while len(dinos) > 0:
        # changing the cactus speed based on score
        cactusSpeed = cactusBaseSpeed + (cactusBaseSpeed * (score / 2000))

        if doClose() == False:
            quit()

        pipe_ind = 0
        if len(dinos) > 0:
            if len(enemies) > 1 and enemies[0].x > enemies[0].x + cactusWidth:
                pipe_ind = 1

        timeSinceLastCactus = time.time() - lastCactusTime
        if timeSinceLastCactus >= chosenTimeDelay:
            appendEnemy()
            lastCactusTime = time.time()

        for x, dino in enumerate(dinos):
            ge[x].fitness += 0.1
            dino.move()

            # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
            enemyId = enemies[pipe_ind].level
            output = nets[dinos.index(dino)].activate((dino.y, abs(dino.x - enemies[pipe_ind].x), enemyId))

            if output[0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1
                dino.jump()
            elif output[0] < -0.5:
                dino.duck()
        
        rem = []

        for enemy in enemies:
            enemy.move()
            for dino in dinos:
                died = enemy.collision(dino)
                if died:
                    nets.pop(dinos.index(dino))
                    ge.pop(dinos.index(dino))
                    dinos.pop(dinos.index(dino))
            
            if enemy.x + cactusWidth < 0:
                rem.append(enemy)

        if enemies[0].x < -100:
            enemies.remove(enemies[0])
        
        for r in rem:
            enemies.remove(r)

        score += 1
        renderScreen(dinos, enemies)
        clock.tick(gameSpeed)
        pygame.display.update()

def run(config_file):

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-config.txt')
    run(config_path)