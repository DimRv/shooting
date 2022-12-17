import pygame as pg
from random import randint
import sys
import math
import time

pg.init()

sc = pg.display.set_mode((1200, 800))
clock = pg.time.Clock()
pg.mixer.music.load('fon.mp3')
pg.mixer.music.play()

class Warrior:
    def __init__(self, sc):
        self.health = 100
        self.move = 3
        self.war_rect = pg.Rect(1200/2 - 25, 800 / 2  -25, 60, 60)
        self.sc = sc
        self.right_move = False
        self.left_move = False
        self.up_move = False
        self.down_move = False
        self.engle = 0
        self.shoots = False
        self.shootings = []
        self.shoot_speed = 25
        self.shoot_move = 25
        self.n = 0
        self.monster_time = 30
        self.monsters = []
        self.monster_group = pg.sprite.Group()
        self.mon_n = 0
        self.points = 0
        self.exp = 0
        self.level = 1
        self.shoot = pg.mixer.Sound('shoot.mp3')
        self.shout = pg.mixer.Sound('shout.mp3')
        self.goal = pg.mixer.Sound('goal.mp3')
        self.shout_time = 0
        self.mon_shout = pg.mixer.Sound('spider_shout.mp3')
        self.bon_time = 180
        self.bonus = False
        

    def draw_Warrior(self):
        self.war_surf = pg.Surface((60,60), pg.SRCALPHA)
        self.war_surf.convert_alpha()
        self.war_surf.fill((220, 220, 220))
        
        self.war_rec = self.war_surf.get_rect()
        pg.draw.circle(self.war_surf, (150, 150, 200), (30,30), 20)
        pg.draw.rect(self.war_surf, (150, 150, 200), (28, 30, 4,30))
        rot_surf = pg.transform.rotate(self.war_surf, self.engle)
        rot_rect  =  rot_surf.get_rect(center = self.war_rec.center)
        for i in self.monsters:
            self.sc.blit(i.rot_img, i.rect)
        font = pg.font.Font(None, 40)
        font2 = pg.font.Font(None, 25)
        level = font2.render(str(self.level), True , (50,50,50))
        level_pos = level.get_rect(center = (30,30))
        score = font.render("Score: " + str(self.points), True , (50,50,50))
        score_pos = score.get_rect(center = (600, 750))
        description = font2.render("Use arrows to move, use mouse to shoot", True , (150,150,150))
        description_pos = score.get_rect(centery = 750)
        self.sc.blit(score, score_pos)
        self.sc.blit(description, description_pos)
        self.war_surf.blit(rot_surf, rot_rect)
        self.war_surf.blit(level,level_pos)
        self.sc.blit(self.war_surf, self.war_rect)

    def update_Warrior(self):
        if self.right_move:
            self.war_rect.x += self.move
        if self.left_move:
            self.war_rect.x -= self.move
        if self.up_move:
            self.war_rect.y -= self.move
        if self.down_move:
            self.war_rect.y += self.move
        if self.shoots:
            if self.n >= self.shoot_speed:
                self.shoot_weapon()
                self.n = 0
        if len(self.shootings) > 0:
            for i in self.shootings:
                i[1].x += math.sin(math.radians(i[2])) * self.shoot_move
                i[1].y += math.cos(math.radians(i[2])) * self.shoot_move
                if i[1].x < 0 or i[1].x > 1200 or i[1].y < 0 or i[1].y > 800:
                    self.shootings.remove(i)
                for j in self.monsters:
                    if j.rect.colliderect(i[1]):
                        self.goal.play()
                        if self.bonus:
                            self.create_bonus(i[1].x, i[1].y)
                            self.bonus = False
                        j.kill()
                        self.monsters.remove(j)
                        self.points += 10
                        self.exp += 10                            
                        level_up = self.level * 100
                        if self.exp % level_up == 0:
                            self.level += 1
                            self.exp = 0
                            if self.monster_time >= 5:
                                self.monster_time +=  -4
                            if self.shoot_speed >=3:
                                self.shoot_speed += -2
                            self.shoot_move += 2
                            self.mon_n = 0
                        if self.points % 500 ==0:
                            self.bonus = True
                    
                        
                pg.draw.circle(i[0],(255,0,0), (i[1].x, i[1].y), 5)
                self.sc.blit(i[0], i[1])
                pg.display.update()
                
    def shoot_weapon(self):
        surf = pg.Surface((5,5))
        self.shoot_rect = pg.Rect(self.war_rect.centerx, self.war_rect.centery, 5, 5)
        self.shootings.append((surf, self.shoot_rect, self.engle))
        self.shoot.play()
        
    def create_bonus(self, x, y):
        rand = randint(0,1)
        bonuses = ["shoot_speed", "mov"]
        self.bon = bonuses[rand]
        bonus_surf = pg.Surface((50,50))
        bonus_rect = pg.Rect(0,0, 50,50)
        
        pg.draw.rect(bonus_surf, (100,200,200), bonus_rect)
        self.sc.blit(bonus_surf, (x, y))

class Monster(pg.sprite.Sprite):
    def __init__(self, sc, enemy):
        pg.sprite.Sprite.__init__(self)
        self.sc = sc
        self.movement = randint(3, 5)
        self.img = pg.image.load("spider.png").convert_alpha()
        position = [(-50, randint(0, 800)), (randint(0, 1200), -50), (1250, randint(0, 800)), (randint(0, 1200), 850)]
        rand = randint(0,3)        
        self.rect = self.img.get_rect(center = position[rand])
        self.enemy = enemy
        self.add(enemy.monster_group)
        
        #war_x = self.enemy.war_rect.centerx
        #war_y = self.enemy.war_rect.centery
        #x = war_x - self.rect.centerx
        #y = war_y - self.rect.centery
        #self.engle = math.degrees(math.atan2(x,y))

    def update(self):
        war_x = self.enemy.war_rect.centerx
        war_y = self.enemy.war_rect.centery
        mon_x = self.rect.centerx
        mon_y = self.rect.centery
        x = war_x - mon_x
        y = war_y - mon_y
        #self.engle = math.atan2(x,y)
        self.engle = math.degrees(math.atan2(x,y))
        self.rot_img = pg.transform.rotate(self.img, 180 + self.engle)
        rot_rect = self.rot_img.get_rect(center = (self.rect.centerx, self.rect.centery))
        rot_rect.x = rot_rect.x + math.sin(math.radians(self.engle)) * self.movement
        rot_rect.y = rot_rect.y + math.cos(math.radians(self.engle)) * self.movement     
        self.rect = rot_rect
        if self.rect.contains(self.enemy.war_rect):
            self.enemy.shout.play()
            surf = pg.Surface((1200,800))
            surf.fill((100,100,100))
            surf.set_alpha(100)
            font = pg.font.Font(None , 60)
            end = font.render("SPIDERS THANK YOU FOR GRAET DINNER!", True, (200,200,200))
            end_pos = end.get_rect(center = (600, 200))
            lvl = font.render("LEVEL: " + str(self.enemy.level), True, (0,200,0))
            lvl_pos = lvl.get_rect(center = (600, 300))
            score = font.render("SCORE: " + str(self.enemy.points), True, (0,200,0))
            score_pos = score.get_rect(center = (600, 400))
            surf.blit(end, end_pos)
            surf.blit(lvl, lvl_pos)
            surf.blit(score, score_pos)
            sc.blit(surf,(0,0))
            pg.display.update()
            time.sleep(10)
            pg.quit()
            sys.exit()
        #sc.blit(rot_img, self.rect)
        #pg.display.update()
        
        


Warrior = Warrior(sc)
while 1:
    clock.tick(60)
    Warrior.n += 1
    Warrior.mon_n += 1
    Warrior.shout_time += 1
    sc.fill((220, 220, 220))
    Warrior.draw_Warrior()
    Warrior.update_Warrior()
    if Warrior.mon_n == Warrior.monster_time:
        new_monster = Monster(sc, Warrior)
        Warrior.monsters.append(new_monster)
        Warrior.mon_n = 0
    Warrior.monster_group.update()
    if Warrior.shout_time == 1000:
        Warrior.mon_shout.play()
        Warrior.shout_time = 0
    
    for i in pg.event.get():
        if i.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if i.type == pg.KEYDOWN:
            if i.key == pg.K_LEFT:
                Warrior.left_move = True
            if i.key == pg.K_RIGHT:
                Warrior.right_move = True
            if i.key == pg.K_UP:
                Warrior.up_move = True
            if i.key == pg.K_DOWN:
                Warrior.down_move = True
        if i.type == pg.KEYUP:
            if i.key == pg.K_LEFT:
                Warrior.left_move = False
            if i.key == pg.K_RIGHT:
                Warrior.right_move = False
            if i.key == pg.K_UP:
                Warrior.up_move = False
            if i.key == pg.K_DOWN:
                Warrior.down_move = False
        if i.type == pg.MOUSEMOTION:
            pos = i.pos
            Warrior.x = pos[0]
            Warrior.y = pos[1]
            x = pos[0] - Warrior.war_rect.centerx
            y = pos[1] - Warrior.war_rect.centery
            
            Warrior.engle = math.degrees(math.atan2(x,y))
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 1:
                Warrior.shoots = True
                
        if i.type == pg.MOUSEBUTTONUP:
            if i.button == 1:
                Warrior.shoots = False
            
    pg.display.update()
            
            
    
    
