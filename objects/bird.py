import pygame, os
from settings import *

class Bird():
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("assets","bird.png")), (birdWidth, birdHeight))
        
    def move(self, cactusSpeed):
        self.x -= cactusSpeed

    def collision(self, dino):
        collided = False
        if self.x < dino.x + dino.width and self.x + birdWidth > dino.x: # checking if the bird x overlaps with the dino x
            if self.y < dino.y + dino.height and self.y + birdHeight > dino.y:
                collided = True
        return(collided)