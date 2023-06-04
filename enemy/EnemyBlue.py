from enemy.enemy import Enemy
from random import randint
import pygame
from pygame.locals import pygame

class EnemyBlue(Enemy):
    def __init__(self, pos_x, pos_y):
        self.damage = 5
        self.img = pygame.image.load("D:\image\monkey.png")
        self.x = pos_x
        self.y = pos_y
        self.movement_speed = 5