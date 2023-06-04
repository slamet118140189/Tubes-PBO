import pygame
from pygame.locals import *

class Arrow:
    def __init__(self, angle, x, y, img):
        self.angle=angle
        self.x=x
        self.y=y
        self.img=img

    def fire(self, gama):
        new_arrow = pygame.transform.rotate(self.img, 360-self.angle*57.29)
        gama.screen.blit(new_arrow, (self.x, self.y))

    def get_position(self):
        self.rect = pygame.Rect(self.img.get_rect())
        self.rect.top = self.y # ambil titik y 
        self.rect.left = self.x # ambil titik x