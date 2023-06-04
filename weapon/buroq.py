from weapon.weapon import Weapon
from pygame.locals import *
import pygame

class Buroq(Weapon):
    def __init__(self):
        super().__init__()
        self.__damage=100
        self.img=pygame.image.load("D:image\orok.png")
    def get_damage(self):
        return self.__damage