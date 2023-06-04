from weapon.weapon import Weapon
from pygame.locals import *
import pygame

class Bluegun(Weapon):
    def __init__(self):
        super().__init__()
        self.__damage=90
        self.img=pygame.image.load("D:image\panahblue.png")
    def get_damage(self):
        return self.__damage