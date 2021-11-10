import pygame

# SETTINGS
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
scoreColor = (255,255,255)
# 30, 40
birdHeight = 46
birdWidth = 62

# init
clock = pygame.time.Clock()
pygame.mixer.init()

# assets
jumpSound = pygame.mixer.Sound("assets/jump.wav")
jumpSound.set_volume(0.01)

# fonts
pygame.font.init()
font = pygame.font.SysFont("comicsans", 50)

# display
screen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Dino Game')
