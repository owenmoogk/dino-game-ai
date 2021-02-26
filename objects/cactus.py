import pygame, os
from settings import *

class Cactus:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("assets","cactus.png")), (cactusWidth, cactusHeight))

    def move(self, cactusSpeed):
        self.x -= cactusSpeed

    def collision(self, dino):
        collided = False
        if self.x < dino.x + dino.width and self.x + cactusWidth > dino.x: # checking if the cactus x overlaps with the dino x
            if self.y < dino.y + dino.height:
                collided = True
        return(collided)