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
        self.exp = 0
        self.max_hp = initial_hp
        self.hp = self.max_hp
        self.speed = initial_speed
        self.to_x = 0
        self.to_y = 0
        self.weapons = []
    
    def move(self):
        super().move(((self.to_x, self.to_y)))
    
    def gainEXP(self, exp):
        self.exp += exp.exp_amount
        exp_list.remove(exp)
        if self.exp >= 5:
            self.exp = 0
            self.levelUp()
    
    def levelUp(self):
        self.lv += 1

# 몬스터
monster_name_list = ["zero_division", "stack_overflow", "range_out_head"]

class Monster(Object):
    def __init__(self, monster_pos, monster_name, player):
        super().__init__(monster_pos, monster_name)
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
        monster_list.append(self)

        if monster_name == "zero_division":
            stat = [1,3,2]
        if monster_name == "stack_overflow":
            stat = [10,2,4]
        if monster_name == "range_out":
            stat = [5,1,2]
        self.max_hp = stat[0]
        self.hp = self.max_hp
        self.speed = stat[1]
        self.dmg = stat[2]

    def move(self):
        vec_x = self.player.x - self.x
        vec_y = self.player.y - self.y
        side = math.sqrt(vec_y ** 2 + vec_x ** 2)
        super().move(
            (vec_x / side * self.speed, vec_y / side * self.speed))
    
    def die(self):
        EXP(self, "exp")
        monster_list.remove(self)

# 경험치
class EXP(Object):
    def __init__(self, monster, path):
        super().__init__((monster.x + monster.width / 2, monster.y + monster.height / 2), path)
        self.player = monster.player
        self.exp_amount = monster.max_hp
        self.speed = 7
        exp_list.append(self)
    
    def move(self):
        vec_x = self.player.x - self.x
        vec_y = self.player.y - self.y
        side = math.sqrt(vec_y ** 2 + vec_x ** 2)
        if side <= 300:
            super().move(
                (vec_x / side * self.speed, vec_y / side * self.speed))


# 경험치 바
class EXPBar():
    def __init__(self, player, path):
        self.player = player
        self.img = pygame.image.load(os.path.join(image_path, path + ".png"))
        self.img = pygame.transform.scale(self.img, (1, 50))
        self.rect = self.img.get_rect()
        self.rect.left = 0
        self.rect.top = 0

    def resize(self):
        self.img = pygame.transform.scale(self.img, (int(screen_width * (self.player.exp / 5)) + 1, 50))
        self.rect = self.img.get_rect()
        self.rect.left = 0
        self.rect.top = 0

class Weapon:
    def __init__(self, player, path, speed, dmg, atk_speed):
        self.lv = 1
        self.bullet = path
        self.bullet_speed = speed
        self.bullet_dmg = dmg
        self.attack_delay = atk_speed
        self.cnt = 0
        self.player = player
        player.weapons.append(self)
    
    def atk(self):
        if self.cnt == self.attack_delay:
            self.cnt = 0
            return True
        else:
            self.cnt += 1
            return False

    def shotBullet(self):
        if not self.atk():
            return
        p_x = self.player.x
        p_y = self.player.y
        target = None
        dist_min = 1000000
        for monster in monster_list:
            m_x = monster.x
            m_y = monster.y
            dist = (p_x - m_x) ** 2 + (p_y - m_y) ** 2
            if dist < dist_min:
                dist_min = dist
                target = monster
        if target is None:
            return
        else:
            velocity = (target.x - p_x, target.y - p_y)
        x = self.player.x + self.player.width
        y = self.player.y + self.player.height
        Bullet((x, y), self.bullet, velocity, self.bullet_dmg, self.bullet_speed)


class Bullet(Object):
    def __init__(self, maker_pos, path, velocity, dmg, speed):
        super().__init__(maker_pos, path)
        self.x += self.width / 2
        self.y += self.height / 2
        self.img = pygame.transform.scale(self.img, (30, 30))
        self.rect = self.img.get_rect()
        size = self.rect.size
        self.width = size[0]
        self.height = size[1]
        self.x -= self.width / 2
        self.y -= self.height / 2
        self.rect.left = self.x
        self.rect.top = self.y
        self.dmg = dmg
        self.v_x = velocity[0] * speed
        self.v_y = velocity[1] * speed
        player_bullet_list.append(self)

    def move(self):
        self.x += self.v_x
        self.y += self.v_y
        self.rect.left = self.x
        self.rect.top = self.y