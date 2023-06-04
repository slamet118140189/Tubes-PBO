from weapon.weapon import Weapon
from pygame.locals import *
import pygame

class Keju(Weapon):
    def __init__(self):
        super().__init__()
        self.__damage=75
        self.img=pygame.image.load("D:image\keju.png")
    def get_damage(self):
        return self.__damage