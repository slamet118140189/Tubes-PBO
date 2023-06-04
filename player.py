import pygame
import math
from random import randint
from pygame.locals import *
from arrow import Arrow
from weapon.bluegun import Bluegun
from weapon.buroq import Buroq
from weapon.keju import Keju
from weapon.noza import Noza
from weapon.weapon import Weapon

class Player:
    def __init__(self):
        self.playerpos = [100, 100] # initial position for player
        self.img = pygame.image.load("D:image\dude.png")
        self.speed = 5
        self.arrows = []
        self.index_arrow = 0
        self.health_point = 194
        self.weapon=Weapon()
        self.damageweapon = 10
        self.x = 100
        self.y = 100

    def add_arrow(self):
        self.arrows.append(Arrow(self.angle, self.new_playerpos[0]+32, self.new_playerpos[1]+32, self.weapon.img))
    
    def move_arah(self):
        self.mouse_position = pygame.mouse.get_pos()  # pembaruan posisi kursor
        self.angle = math.atan2(self.mouse_position[1] - (self.y+32), self.mouse_position[0] - (self.x+26))
        self.player_rotation = pygame.transform.rotate(self.img, 360 - self.angle * 57.29)
        self.new_playerpos = (self.x - self.player_rotation.get_rect().width/2, self.y - self.player_rotation.get_rect().height/2)
    
    def move(self, value, tombol):
        if tombol == "w" and self.y > 100:
            self.y -= 5
        elif tombol == "s" and self.y < 420:
            self.y += 5 
        if tombol == "a" and self.x > 100:
            self.x -= 5
        elif tombol == "d" and self.x < 480:
            self.x += 5
    
    def kurangi_healthpoint(self):
        self.health_point -= randint(5, 20)
        self.get_healthpoint()

    def get_healthpoint(self):
        # print(self.health_point)
        return self.health_point
    
    def get_position(self):
        self.rect = pygame.Rect(self.img.get_rect())
        self.rect.top = self.y # ambil titik y 
        self.rect.left = self.x # ambil titik x