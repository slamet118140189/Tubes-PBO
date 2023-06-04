from enemy.enemy import Enemy
from random import randint
import pygame
from pygame.locals import pygame

class EnemyOrange(Enemy):
    def __init__(self, pos_x, pos_y):
        self.damage = 2
        self.img = pygame.image.load("D:\image\musuh.png")
        self.x = pos_x
        self.y = pos_y
        self.movement_speed = 2

