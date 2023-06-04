from weapon.weapon import Weapon
from pygame.locals import *
import pygame

class Noza(Weapon):
    def __init__(self):
        super().__init__()
        self.__damage=60
        self.img=pygame.image.load("D:image\gunnoza.png")
    def get_damage(self):
        return self.__damage