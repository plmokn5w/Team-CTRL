import pygame
import os
import math
import random

# 화면 크기
screen_width = 800
screen_height = 500
# 파일 경로
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "../images")

# 게임 종료 메시지
# time out
# mission complete
# game over
game_result = "Game over"

# 오브젝트 리스트
player_bullet_list = []
monster_list = []
monster_bullet_list = []
exp_list = []

class Object:
    def __init__(self, initial_pos, path):
        self.img = pygame.image.load(os.path.join(image_path, path + ".png"))
        self.rect = self.img.get_rect()
        size = self.rect.size
        self.width = size[0]
        self.height = size[1]
        self.x = initial_pos[0] - self.width / 2
        self.y = initial_pos[1] - self.height / 2
        self.rect.left = self.x
        self.rect.top = self.y
    
    def move(self, to_pos):
        self.x += to_pos[0]
        self.y += to_pos[1]
        self.rect.left = self.x
        self.rect.top = self.y
    
    def collide(self, obj):
        return self.rect.colliderect(obj.rect)

# 플레이어
class Player(Object):
    def __init__(self, character_name,
                 initial_hp, initial_speed):
        super().__init__((screen_width / 2, screen_height / 2), character_name)
        self.lv = 0
        self.max_hp = initial_hp
        self.hp = self.max_hp
        self.speed = initial_speed
        self.to_x = 0
        self.to_y = 0
        self.weapons = []
    
    def move(self):
        super().move((self.to_x, self.to_y))
    
    def gain_exp(self, exp):
        self.lv += exp.exp_amount
        exp_list.remove(exp)

# 몬스터
monster_name_list = ["zero_division", "stack_overflow", "range_out_head"]

class zero_division(Object):
    def __init__(self,monster_pos, player):
        super().__init__(monster_pos,"zero_division")
        self.player = player
        self.x += self.width / 2
        self.y += self.height / 2
        self.img = pygame.transform.scale(self.img, (70, 70))
        self.rect = self.img.get_rect()
        size = self.rect.size
        self.width = size[0]
        self.height = size[1]
        self.x -= self.width / 2
        self.y -= self.height / 2
        self.rect.left = self.x
        self.rect.top = self.y
        self.max_hp = 1
        self.hp = self.max_hp
        self.speed = 3
        self.dmg = 2
        self.shoot_count=0
        self.shoot_act=50
        monster_list.append(self)

    def move(self):
        self.shoot_count+=1
        if self.shoot_count>=self.shoot_act:
            self.shoot()
            self.shoot_count=0
        distance = math.sqrt((self.x - self.player.x) ** 2 + (self.y - self.player.y) ** 2)
        vec_x = self.player.x - self.x
        vec_y = self.player.y - self.y
        side = math.sqrt(vec_y ** 2 + vec_x ** 2)
        if 200 + 3 < distance:
            super().move((vec_x / side * self.speed, vec_y / side * self.speed))
        elif 200 - 3 > distance:
            super().move((vec_x / side * -self.speed, vec_y / side * -self.speed))
    def shoot(self):
        bullet((self.x,self.y),self.player)

    def die(self):
        EXP(self,"exp")
        monster_list.remove(self)

class bullet(Object):
    def __init__(self, monster_pos,player):
        super().__init__(monster_pos, "bullet")
        self.speed=4
        self.player=player
        self.x=monster_pos[0]
        self.y=monster_pos[1]
        vec_x = player.x - self.x
        vec_y = player.y - self.y
        side = math.sqrt(vec_y ** 2 + vec_x ** 2)
        self.vector=(vec_x/side*self.speed,vec_y/side*self.speed)#(math.atan2(vec_y,vec_x)*180/math.pi)
        self.img=pygame.transform.rotate(self.img,math.atan(vec_x/vec_y)*180/math.pi)
        self.img=pygame.transform.scale(self.img,(10, 30))
        self.rect = self.img.get_rect()
        monster_bullet_list.append(self)

    def move(self):
        if (math.sqrt((self.x - self.player.x) ** 2 + (self.y - self.player.y) ** 2)>=800):
            monster_bullet_list.remove(self)
        else:
            super().move(self.vector)

class stack_overflow(Object):
    def __init__(self, monster_pos, player):
        super().__init__(monster_pos, "stack_overflow")
        self.player = player
        self.x += self.width / 2
        self.y += self.height / 2
        self.img = pygame.transform.scale(self.img, (100, 100))
        self.rect = self.img.get_rect()
        size = self.rect.size
        self.width = size[0]
        self.height = size[1]
        self.x -= self.width / 2
        self.y -= self.height / 2
        self.rect.left = self.x
        self.rect.top = self.y
        self.max_hp = 10
        self.hp = self.max_hp
        self.speed = 1
        self.dmg = 4
        monster_list.append(self)

    def move(self):
        vec_x = self.player.x - self.x
        vec_y = self.player.y - self.y
        side = math.sqrt(vec_y ** 2 + vec_x ** 2)
        super().move((vec_x / side * self.speed, vec_y / side * self.speed))

    def die(self):
        EXP(self, "exp")
        monster_list.remove(self)

class range_out(Object):
    def __init__(self, monster_pos, player):
        super().__init__(monster_pos, "range_out")
        self.player = player
        self.x += self.width / 2
        self.y += self.height / 2
        self.img = pygame.transform.scale(self.img, (70, 70))
        self.rect = self.img.get_rect()
        size = self.rect.size
        self.width = size[0]
        self.height = size[1]
        self.x -= self.width / 2
        self.y -= self.height / 2
        self.rect.left = self.x
        self.rect.top = self.y
        self.max_hp = 5
        self.hp = self.max_hp
        self.speed = 2
        self.dmg = 3
        self.body=[range_out_body((self.x,self.y), self)]
        for i in range(9):
            self.body.append(range_out_body((self.x,self.y), self.body[i]))
        monster_list.append(self)
    def collide(self, obj):
        if self.rect.colliderect(obj.rect):
            return True
        for body in self.body:
            if body.collide(obj):
                return True
        return False
    def move(self):
        vec_x = self.player.x - self.x
        vec_y = self.player.y - self.y
        side = math.sqrt(vec_y ** 2 + vec_x ** 2)
        super().move((vec_x / side * self.speed, vec_y / side * self.speed))
        #self.img=pygame.transform.rotate(self.img,(vec_x/vec_y))
        for body in self.body:
            body.move(self.speed)
    def paint(self,screen):
        for body in self.body[-1:]:
            screen.blit(body.img,(body.x, body.y))
    def die(self):
        EXP(self, "exp")
        monster_list.remove(self)
        for body in self.body:
            monster_list.remove(body)

class range_out_body(Object):
    def __init__(self,monster_pos, front):
        super().__init__(monster_pos,"range_out_body")
        self.front = front
        self.x += self.width / 2
        self.y += self.height / 2
        self.img = pygame.transform.scale(self.img, (70, 70))
        self.rect = self.img.get_rect()
        size = self.rect.size
        self.width = size[0]
        self.height = size[1]
        self.x -= self.width / 2
        self.y -= self.height / 2
        self.rect.left = self.x
        self.rect.top = self.y
        monster_list.append(self)
    def move(self, speed):
        vec_x = self.front.x - self.x
        vec_y = self.front.y - self.y
        side = math.sqrt(vec_y ** 2 + vec_x ** 2)
        if 40 + 3 < side != 0:
            super().move((vec_x / side * speed, vec_y / side * speed))
        elif 40 - 3 > side != 0:
            super().move((vec_x / side * -speed, vec_y / side * -speed))
    def collide(self, obj):
        return self.rect.colliderect(obj.rect)
# 경험치
class EXP(Object):
    def __init__(self, monster, path):
        super().__init__((monster.x, monster.y), path)
        self.player = monster.player
        self.exp_amount = monster.max_hp
        self.speed = 10
        exp_list.append(self)
    
    def move(self):
        vec_x = self.player.x - self.x
        vec_y = self.player.y - self.y
        side = math.sqrt(vec_y ** 2 + vec_x ** 2)
        if side <= 100:
            super().move(
                (vec_x / side * self.speed, vec_y / side * self.speed))

class Weapon:
    def __init__(self):
        pass

class Bullet(Object):
    def __init__(self, maker_pos, path):
        super().__init__(maker_pos, path)
