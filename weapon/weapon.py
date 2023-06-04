from pygame.locals import *
import pygame

class Weapon:
    def __init__(self):
        self.__damage=50
        self.img=pygame.image.load("D:image\panah.png")
    def get_damage(self):
        return self.__damage