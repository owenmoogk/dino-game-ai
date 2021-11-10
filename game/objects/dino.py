import pygame, os, time, sys, keyboard
from random import uniform, randint
from settings import *

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