from enemy.enemy import Enemy
from random import randint
import pygame
from pygame.locals import pygame

class Boss(Enemy):
    def __init__(self, pos_x, pos_y, hp):
        self.img = pygame.image.load("D:\image\oss.png")
        self.x = pos_x
        self.y = pos_y
        self.movement_speed = 3
        self.hop = hp

    def attack(self, player):
        player.health_point = 0