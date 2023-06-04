from player import Player
import pygame
import math
from random import randint

class Buff():
    def __init__(self, x, y):
        self.plus_damage = 0
        self.waktubuff = 100
        self.img = pygame.image.load("D:\image\musuhh.png")
        self.x= x
        self.y=y
    
    def get_rect(self):
        self.rect = pygame.Rect(self.img.get_rect())
        self.rect.top = self.y # ambil titik y 
        self.rect.left = self.x # ambil titik x

    def move(self):
        self.y+=1
        self.get_rect()

    def attack(self, player):
        player.health_point -= self.damage
