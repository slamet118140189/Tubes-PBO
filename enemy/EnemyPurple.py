from enemy.enemy import Enemy
from random import randint
import pygame
from pygame.locals import pygame

class EnemyPurple(Enemy): 
    def __init__(self, pos_x, pos_y):
        self.damage = 10
        self.img = pygame.image.load("D:\image\epet.png")
        self.x = pos_x
        self.y = pos_y
        self.movement_speed = 5

