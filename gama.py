import pygame
import math
from random import randint
from pygame.locals import *
from player import Player
from arrow import Arrow
from enemy.EnemyOrange import EnemyOrange
from enemy.EnemyPurple import EnemyPurple
from enemy.EnemyBlue import EnemyBlue
from enemy.boss import Boss
import random
import time
from level import Level, Easy, Medium, Hard
from buff import Buff
from weapon.bluegun import Bluegun
from weapon.buroq import Buroq
from weapon.keju import Keju
from weapon.noza import Noza
from weapon.weapon import Weapon

import button
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.username = None
        self.width = 640
        self.height = 480
        self.screen = pygame.display.set_mode((self.width, self.height)) #Membuat window game 640x480
        self.clock = pygame.time.Clock()
        self.gameover = pygame.image.load("D:\image\gameover.png") #Load image gameover
        self.youwin = pygame.image.load("D:\image\youwin.png")
        self.tamat = pygame.image.load("D:\image\ytamat.png")
        self.healthbar = pygame.image.load("D:\image\healthbar.png")
        self.health = pygame.image.load("D:\image\health.png")
        self.castle = pygame.image.load("D:\image\castle.png")
        self.usernameimage = pygame.image.load("D:\\image\\username.png")
        self.countdown_timer = 60000 #Run game 60 detik
        self.fontusername = pygame.font.Font("Astonpoliz.ttf", 28)
        self.font = pygame.font.Font(None, 24)
        self.player = Player()
        self.buff=[]
        self.bos = []
        self.enemies=[]
        self.enemy_timer = 100
        self.fps = 60         
        self.__score = 0
        self.seconds = 0
        self.exitcode = 0
        self.EXIT_CODE_GAME_OVER = 0
        self.EXIT_CODE_WIN = 1
        self.boss_round=False
        self.level = Easy()
        self.waktu_restart = 0
        self.time_rounde = 0
        self.munculbuff = 250
        self.timefirstrun=True
        self.first = 1
        self.darah_boss = True
        self.highscore = 0
        self.timeweapon = 999
        self.setdisplay = pygame.display.set_caption("JOGBEN PRODUCTION")
        
    def get_score(self):
        return self.__score
    
    def tambah_score(self):
        self.__score += 1
    
    def reset_score(self):
        self.__score = 0

    #Melakukan pengecekan panah, serta menghapus dan menampilkan panah
    def checking_arrow(self):
        for panah in self.player.arrows:
            arrow_index = 0
            panah.x+=math.cos(panah.angle)*10
            panah.y+=math.sin(panah.angle)*10
            if panah.x < -64 or panah.x > self.width or panah.y < -64 or panah.y > self.height:
                self.player.arrows.pop(arrow_index)
            arrow_index+=1
            for projectline in self.player.arrows:
                projectline.fire(self)

    #Mengeluarkan musuh dan boss
    def spawn_enemy(self):
        new_enemy = None
        timer=randint(1,100)
        self.enemy_timer -= 1
        # print("Waktu Sekarang: {}".format(self.seconds))
        if(self.seconds==40 or self.seconds==15): #Boss akan keluar di detik ke-50 dan detik ke-20. kemunculan boss per-level terjadi hanya 2x
            self.boss_round=True
        if(self.enemy_timer==0):
            boss = False
            if(self.boss_round):
                hp = self.level.hp_boss()
                new_enemy=Boss(self.width, randint(50, self.height-63), hp)
                timer=100
            else:
                now_level = self.level.get_level()
                if (now_level == Easy):
                    new_enemy = EnemyOrange(self.width, randint(50, self.height-43)) #Memunculkan musuh tergantung pada level easy
                elif (now_level == Medium):
                    new_enemy = EnemyBlue(self.width, randint(50, self.height-43)) #Memunculkan musuh tergantung pada level medium
                else:
                    new_enemy = EnemyPurple(self.width, randint(50, self.height-43)) #Memunculkan musuh tergantung pada level hard            
            new_enemy=self.enemies.append(new_enemy) #menambahkan musuh ke dalam list musuh
            self.enemy_timer=timer
        self.boss_round=False

        for enemy in self.enemies:
            self.screen.blit(enemy.img, (enemy.x, enemy.y)) #menampilkan musuh sebanyak musuh yang ada di dalam list

    #melakukan pengecekan musuh apakah terkena panah atau musuh sudah sampai benteng
    def checking_enemies(self):
        index=0
        self.darah_boss = True
        for enemy in self.enemies:
            enemy.move(self.player, enemy) #memanggil method move pada class Enemy
            if(enemy.x < 64): #Melakukan pengecekan apakah musuh pada titik x lebih kecil dari 64
                if(self.load_audio):
                    self.hit_sound.play()
                self.enemies.pop(index) #jika titik x musuh sudah lebih kecil dari 64, musuh di hapus dari list musuh
            index_arrow = 0
            for bullet in self.player.arrows:
                bullet.get_position() #Mendapatkan posisi x dan y dari peluru/panah
                enemy.get_rect() #mendapatkan posisi x dan y dari musuh/enemy
                if enemy.rect.colliderect(bullet.rect): #melakukan pengecekan apakah musuh dan panah sedang bertabrakan
                    if(self.load_audio):
                        self.enemy_hit_sound.play()
                    # self.score += 1 #melakukan penambahan score, jika peluru/panah terkena musuh ditambah 1 
                    if(isinstance(enemy,Boss)): #melakukan pengecekan apakah musuh yang terkena panah itu adalah boss dengan menggunakan isinstance
                        # print(self.player.weapon.get_damage())
                        enemy.hop -= self.player.weapon.get_damage() #melakukan pengurangan darah boss, dari damage senjata yang dipakai
                        self.darah_boss = False
                        if(enemy.hop <= 0 ): #melakukan pengecekan apakah darah boss lebih kecil atau sama dengan 0
                            self.boss_round=False
                            self.darah_boss = True
                    if (self.darah_boss and len(self.enemies)>0): #melakukan pengecekan, apakah self.darah_boss bernilai True dan apakah list musuh tidak kosong
                        self.tambah_score()
                        self.enemies.pop(index) #melakukan pengahapusan musuh sesuai dengan indexnya sekarang 
                    self.player.arrows.pop(index_arrow) #melakukan pengahapusan panah/peluru sesuai dengan indexnya sekarang
                index_arrow += 1
            index += 1
    
    #Mengeluarkan buff atau random senjata
    def spambuff(self):
        # print(self.munculbuff)
        self.munculbuff -= 1 #pengurangan nilai atribut munculbuff, atribut munculbuff di inisialisasi awal bernilai 1000 dan dilakukan pengurangan 1 
        if(self.munculbuff == 0): #melakukan pengecekan apakah nilai dari atribut munculbuff sama dengan 0
            new_buff = Buff(randint(170, self.width-100), 50) #memanggil class buff dengan dua parameter yang dikirim ke class buff 
            self.buff.append(new_buff) #menambahkan objek buff ke dalam list self.buff
            self.munculbuff = 750 
        for buff in self.buff:
            self.screen.blit(buff.img, (buff.x, buff.y)) #menampilkan buff ke layar game sesuai dengan titik x dan titik y, yang dimiliki buff itu

    #membuat tampilan menu, ketika pertama kali memulai game
    def menu(self):
        self.load_audio = True #melakukan inisialiasi awal atribut self.load_audio ke True
        self.textaudio = "ON"
        self.backgroundmenu = pygame.image.load('D:\image\menugame.png').convert_alpha() #Melakukan load gambar
        start_img = pygame.image.load('D:\image\start_btn.png').convert_alpha()
        exit_img = pygame.image.load('D:\image\exit_btn.png').convert_alpha()
        audio_on = pygame.image.load('D:\image\on.png').convert_alpha()
        audio_off = pygame.image.load('D:\image\off.png').convert_alpha()

        start_button = button.Button(195, 305, start_img, 0.8) 
        exit_button = button.Button(350, 308, exit_img, 0.8)
        audio_on = button.Button(7, 10, audio_on, 0.8)
        audio_off = button.Button(7, 60, audio_off, 0.8)

        pygame.mixer.music.load("D:\image\moonlight.wav")
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.25) 

        run = True
        while run: 
            self.screen.blit(self.backgroundmenu, (0, 0)) #Menampilkan background dari menu game dengan titik x bernilai 0 dan titik y bernilai 0
            if start_button.draw(self.screen): #melakukan pemanggilan methode draw yang ada pada class Button
                pygame.mixer.music.stop()
                self.run() #memanggil fungsi run jika tombol play di klik
            if exit_button.draw(self.screen):
                sys.exit() #melakukan fungsi exit yang terdapat pada module sys untuk keluar dalam program yang sedang berjalan jika tombol exit di klik
            if audio_on.draw(self.screen):
                pygame.mixer.music.play(-1, 0.0)
                self.textaudio = "ON"
                self.load_audio = True
            if audio_off.draw(self.screen):
                pygame.mixer.music.stop()
                self.textaudio = "OFF"
                self.load_audio = False
            text = self.font.render("SOUND: {}".format(self.textaudio), True, (255, 255, 255)) #Membuat teks dengan warna putih
            textRect = text.get_rect()
            textRect.centerx = self.screen.get_rect().centerx + 270
            textRect.centery = self.screen.get_rect().centery - 222
            self.screen.blit(text, textRect) #menampilkan text pada pojok kanan atas, titik kordinat dari textRect.centerx dan textRect.centery
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            pygame.display.update()
        pygame.quit()

    #Melakukan pengecekan buff, apakah terdapat buff di dalam game
    def checking_buff(self):
        for buf in self.buff:
            buf.move() #memanggil method move yang terdapat pada class buff
            buf.get_rect() #memanggil method get_rect yang terdapat pada class buff
            if buf.y > 470: #melakukan pengecekan apakah buff sudah sampai bawah atau titik y dari buff sudah lebih besar dari 470 
                if(self.load_audio):
                    self.hit_sound.play()
                self.buff.remove(buf) #menghapus buff dalam list dengan parameter dari buff itu sendiri
            self.player.get_position()
            if buf.rect.colliderect(self.player.rect):
                if(self.load_audio):
                    self.enemy_hit_sound.play()
                self.buff.remove(buf)  # Menghapus objek dari daftar menggunakan remove()
                weapone = [Bluegun(), Buroq()]
                random_weapon = random.choice(weapone)
                self.player.weapon = random_weapon
                self.timeweapon = 1000
                self.buffactive = True
            index_arrow = 0
            for bullet in self.player.arrows:
                bullet.get_position() #mendapatkan posisi panah/peluru
                buf.get_rect() #mendapatkan posisi buff
                if buf.rect.colliderect(bullet.rect): #melakukan pengecekan apakah panah/peluur mengenai buff
                    weapone = [Keju(), Noza()] #membuat list dengan isinya sebuah class
                    random_weapon = random.choice(weapone) #melakukan random dari list weapon, untuk mendapatkan buff secara random
                    self.player.weapon = random_weapon #melakukan inisialisasi atribut weapon pada class player sesuai dengan nilai random yang di dapat
                    self.timeweapon = 1000
                    self.buffactive = True
                    if(self.load_audio): #melakukan load audio jika self.load_audio = True
                        self.enemy_hit_sound.play()
                    self.buff.remove(buf)
                    self.player.arrows.pop(index_arrow)
                index_arrow += 1

    def resetweapon(self):
        # print(self.timeweapon)
        self.timeweapon -= 1
        if (self.timeweapon < 0 and self.buffactive):
            self.player.weapon = Weapon()
            self.buffactive = False
    
    #membuat method kalah        
    def kalah(self):
        self.screen.fill(0) #Merubah warna layar menjadi full hitam
        self.screen.blit(self.gameover, (0, 0)) #menampilkan gambar dari atribut gameover
        text = self.fontusername.render("SCORE: {}".format(self.get_score()), True, (255, 255, 255)) #membuat text SCORE dengan warna putih
        textRect = text.get_rect()
        textRect.centerx = self.screen.get_rect().centerx
        textRect.centery = self.screen.get_rect().centery + 90
        self.screen.blit(text, textRect)
        pygame.display.flip()
        rest = True
        while rest:
            for event in pygame.event.get(): #melakukan looping untuk menerima inputan dari keyboard
                if event.type == pygame.QUIT: #Jika melakukan klik pada tombol exit yang ada di pojok kanan atas
                    pygame.quit()
                    exit(0)
            restart = pygame.key.get_pressed()
            if restart[pygame.K_SPACE]: #jika tombol spasi di tekan
                self.restart()
                rest = False #membuat nilai dari rest menjadi false agar bisa keluar dari looping while
        self.run() #menjalankan method run

    #membuat method menang
    def menang(self, now_level): #menerima parameter level sekarang
        if(now_level == Hard): #jika level sama dengan hard, akan menuliskan nilai dari score ke dalam sebuah notepad atau file txt
            file_score = open("D:/image/scorelist.txt", "a")
            file_score.write("\n{} : {}".format(self.username, str(self.get_score())))
            file_score.close()
        rest = True
        while rest:
            if(now_level == Hard): #jika level sama dengan hard
                self.screen.blit(self.tamat, (0, 0)) #menampilkan image tamat, dengan ukuran image 640x480
                text = self.fontusername.render("SCORE AKHIR: {}".format(self.get_score()), True, (255, 255, 255)) #membuat text SCORE AKHIR dengan warna putih
                textRect = text.get_rect()
                textRect.centerx = self.screen.get_rect().centerx
                textRect.centery = self.screen.get_rect().centery + 35
                self.screen.blit(text, textRect) 
                pygame.display.flip()
                if(self.highscore <= self.get_score()):
                    self.highscore = self.get_score()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit(0)
                    restart = pygame.key.get_pressed()
                    if restart[pygame.K_SPACE]:
                        rest = False
                        self.restart_tamat()
            else:
                self.screen.blit(self.youwin, (0, 0))
                pygame.display.flip()
    
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            pygame.quit()
                            exit(0)
                    restart = pygame.key.get_pressed()
                    if restart[pygame.K_SPACE]:
                        self.restart()
                        rest = False
                    elif restart[pygame.K_RETURN]:
                        self.change_level(self.level.get_level())
                        self.next()
                        rest = False
        self.run()

    def LoadAudio(self):
        pygame.mixer.init()
        self.hit_sound = pygame.mixer.Sound("D:\image\explode.wav")
        self.enemy_hit_sound = pygame.mixer.Sound("D:\image\enemy.wav")
        self.shoot_sound = pygame.mixer.Sound("D:\image\shoot.wav")
        self.hit_sound.set_volume(0.05)
        self.enemy_hit_sound.set_volume(0.05)
        self.shoot_sound.set_volume(0.05)

    def Backsound(self):
        pygame.mixer.music.load("D:\image\moonlight.wav")
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.25)

    def change_level(self, now_level):
        if (now_level == Easy):
            self.level = Medium()
        elif (now_level == Medium):
            self.level = Hard()
        else:
            pass
            # print("ANDA TAMATT")

    def restart_tamat(self):
        self.player.health_point = 194
        self.enemies.clear()
        self.timefirstrun = True
        self.first = 1
        self.countdown_timer = 60000 
        self.enemy_timer = 100
        self.reset_score()
        self.level = Easy()
        self.munculbuff = 750
        self.player.weapon = Weapon()
        self.buff.clear()
        self.waktu_restart = pygame.time.get_ticks()
        self.buffactive = False
    
    def restart(self):
        self.player.health_point = 194
        self.enemies.clear()
        self.timefirstrun = False
        self.countdown_timer = 60000 
        self.enemy_timer = 100
        self.reset_score()
        self.level = Easy()
        self.munculbuff = 750
        self.player.weapon = Weapon()
        self.buff.clear()
        self.waktu_restart = pygame.time.get_ticks()
        self.buffactive = False
    
    def next(self):
        self.buff.clear()
        self.player.health_point = 194
        self.enemies.clear()
        self.timefirstrun = False
        self.countdown_timer = 60000
        self.player.weapon = Weapon()
        self.enemy_timer = 100
        self.munculbuff = 750
        self.waktu_restart = pygame.time.get_ticks()
        self.buffactive = False

    def text_boss(self):
        for enemy in self.enemies:
            if (isinstance(enemy, Boss)):
                boss_text = "HP : {}".format(enemy.hop)
                bosshp = self.font.render(boss_text, True, (255,255,255))
                scoreRect = bosshp.get_rect()
                scoreRect.topright = [440, 10]
                self.screen.blit(bosshp, scoreRect)

    def texthighscore(self):
        if (self.highscore != 0):
            highscore_text = "High Score : {}".format(self.highscore)
            highscoree = self.font.render(highscore_text, True, (255,255,255))
            highRect = highscoree.get_rect()
            highRect.topright = [350, 10]
            self.screen.blit(highscoree, highRect)
    
    def draw_text(self, user):
        username = self.fontusername.render(user.upper(), True, (173, 216, 230))
        username_width = username.get_width()
        self.screen.blit(username, (self.width/2 - (username_width/2), 330))
 
    def set_username(self):
        pygame.mixer.music.load("D:\image\moonlight.wav")
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.25) 
        self.screen.fill(0)
        text = ""
        run = True
        while run:
            self.screen.blit(self.usernameimage, (0, 0))
            self.draw_text(text)  # Menampilkan teks terakhir terpisah dari list `text`
            for event in pygame.event.get():
                if event.type == pygame.TEXTINPUT:
                    text += event.text  # Menambahkan teks ke variabel `text`
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]  # Menghapus karakter terakhir dari variabel `text`
                    elif event.key == pygame.K_RETURN:
                        run = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False

            pygame.display.flip()
        
        self.username = text.upper()
        pygame.mixer.music.stop()
        self.menu()
    
    def run(self):
        if(self.load_audio):
            self.LoadAudio()
            self.Backsound()
        
        running = True
        # print(self.highscore)

        while running:
            if(self.timefirstrun and self.first == 1):
                timerin = pygame.time.get_ticks()
                self.first = 0
                self.time_rounde = 0
                print("awal")
            else:
                self.time_rounde = pygame.time.get_ticks() - self.waktu_restart
                print("akhir")
            
            self.clock.tick(self.fps)
            self.screen.fill(0)
            self.level.background(self)

            for y in range(40, 371, 110):
                self.screen.blit(self.castle, (0, y))

            self.player.move_arah()
            self.screen.blit(self.player.player_rotation, self.player.new_playerpos)

            self.screen.blit(self.healthbar, (5,5))
            for hp in range(self.player.health_point):
                self.screen.blit(self.health, (hp+8, 8))

            self.text_boss()
            self.texthighscore()
            self.checking_arrow()
            self.spawn_enemy()
            self.checking_enemies()
            self.resetweapon()
            self.spambuff()
            self.checking_buff()

            if(self.timefirstrun):
                # print("Awal")
                # pygame.time.wait(3000)
                self.seconds = int(((timerin - pygame.time.get_ticks()) + self.countdown_timer)/1000%60)
            else:
                self.seconds = int((self.countdown_timer - self.time_rounde)/1000%60)
            if self.time_rounde > 60000:
                self.seconds = int((0)/1000%60)
            time_text = "Time : {:02}".format(self.seconds)
            clock = self.font.render(time_text, True, (255,255,255))
            textRect = clock.get_rect()
            textRect.topright = [625, 10]
            self.screen.blit(clock, textRect)

            score_text = "Score : {}".format(self.get_score())
            scoree = self.font.render(score_text, True, (255,255,255))
            scoreRect = scoree.get_rect()
            scoreRect.topright = [525, 10]
            self.screen.blit(scoree, scoreRect)

            pygame.display.flip() # memperbarui tampilan game

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.player.add_arrow()
                    if(self.load_audio):
                        self.shoot_sound.play()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.player.move(-1, "a")
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.player.move(1, "d")
                elif keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.player.move(-1, "w")
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.player.move(1, "s")
            
            print(self.time_rounde)

            if self.time_rounde > self.countdown_timer:
                running = False
                self.exitcode = self.EXIT_CODE_WIN
            if self.player.health_point <= 0:
                running = False
                self.exitcode = self.EXIT_CODE_GAME_OVER

        if self.exitcode == self.EXIT_CODE_GAME_OVER:
            self.kalah()
        else:
            self.menang(self.level.get_level())
        
game = Game()
game.set_username()