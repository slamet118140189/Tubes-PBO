import pygame
import math
from random import randint
from pygame.locals import *

from abc import ABC, abstractmethod

class Level(ABC):
    @abstractmethod
    def background(self):
        pass

    @abstractmethod
    def speed_enemy(self):
        pass

    @abstractmethod
    def get_level(self):
        pass

    @abstractmethod
    def hp_boss(self):
        pass

class Easy(Level):
    def __init__(self):
        self.latatbelakang = pygame.image.load("D:\image\easy.png")
        self.name_level = Easy

    def background(self, game):
        game.screen.blit(self.latatbelakang, (0, 0))

    def speed_enemy(self, enemy):
        enemy.movement_speed = 1
        return enemy.movement_speed

    def get_level(self):
         return self.name_level
    
    def hp_boss(self):
         return 250

class Medium(Level):
    def __init__(self):
        self.latatbelakang = pygame.image.load("D:\image\medium.png")
        self.name_level = Medium

    def background(self, game):
        game.screen.blit(self.latatbelakang, (0, 0))

    def speed_enemy(self, enemy):
        enemy.movasyement_speed = 2
        return enemy.movement_speed
    
    def get_level(self):
         return self.name_level

    def hp_boss(self):
         return 500  
    
class Hard(Level):
    def __init__(self):
        self.latatbelakang = pygame.image.load("D:\image\hard.png") 
        self.name_level = Hard

    def background(self, game):
        game.screen.blit(self.latatbelakang, (0, 0))

    def speed_enemy(self, enemy):
        enemy.movement_speed = 1
        return enemy.movement_speed
    
    def get_level(self):
         return self.name_level
    
    def hp_boss(self):
         return 1000