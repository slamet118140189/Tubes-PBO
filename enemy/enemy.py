import pygame
import math
from random import randint
from pygame.locals import *
from player import Player
from level import Level, Easy, Medium, Hard

class Enemy:
    def __init__(self, pos):
        self.enemy_timer = 100
        self.pos = pos

    def hit_tower(self):
        if self.rect.left < 64:
            return True
    
    def get_rect(self):
        self.rect = pygame.Rect(self.img.get_rect())
        self.rect.top = self.y # ambil titik y 
        self.rect.left = self.x # ambil titik x

    def move(self, player, enemy):
        self.x-=enemy.movement_speed
        self.get_rect()
        if(self.hit_tower()):
            self.attack(player)

    def attack(self, player):
        player.health_point -= self.damage