import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()
screen = pygame.display.set_mode((640, 480))
BORDER_LIMIT=5
screen.set_clip(100,100,300,300)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
            
    randcol=(randint(0,255),randint(0,255),randint(0,255))
    for i in range(1):
        rand_pos=(randint(BORDER_LIMIT,640-BORDER_LIMIT),randint(BORDER_LIMIT,640-BORDER_LIMIT))
        screen.set_at(rand_pos,randcol)
    pygame.display.update()