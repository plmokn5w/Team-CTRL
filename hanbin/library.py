import pygame
import os
import math
import random

# 화면 크기
screen_width = 1280
screen_height = 800
# 파일 경로
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "../images")

# 게임 종료 메시지
# time out
# mission complete
# game over
game_result = "Game over"

# 오브젝트 리스트
object_list = []
player_bullet_list = []
monster_list = []
monster_bullet_list = []
exp_list = []
background_list = []


# 배경이 무한대로 나오게 하기 위한 리스트

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

    def collide(self, obj):
        return self.rect.colliderect(obj.rect)

    def move(self, to_pos):
        self.x += to_pos[0]
        self.y += to_pos[1]
        self.rect.left = self.x
        self.rect.top = self.y

    def notplayer(self):
        if self not in object_list:
            object_list.append(self)

    def movebackground(self, to_x, to_y):  # 주인공이 움직이면 다른 애들이 그 반대방향으로 움직인다
        self.x -= to_x
        self.y -= to_y
        self.rect.left = self.x
        self.rect.top = self.y


# 플레이어
class Player(Object):
    def __init__(self, character_name, initial_hp, initial_speed):
        super().__init__((screen_width / 2, screen_height / 2), character_name)
        self.lv = 0
        self.max_hp = initial_hp
        self.hp = self.max_hp
        self.speed = initial_speed
        self.to_x = 0
        self.to_y = 0
        self.weapons = []

    def gain_exp(self, exp):
        self.lv += exp.exp_amount
        exp_list.remove(exp)
        object_list.remove(exp)


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
            stat = [1, 3, 2]
        if monster_name == "stack_overflow":
            stat = [10, 2, 4]
        if monster_name == "range_out":
            stat = [5, 1, 2]
        self.max_hp = stat[0]
        self.hp = self.max_hp
        self.speed = stat[1]
        self.dmg = stat[2]

    def monmove(self):
        vec_x = self.player.x - self.x
        vec_y = self.player.y - self.y
        side = math.sqrt(vec_y ** 2 + vec_x ** 2)
        super().move((vec_x / side * self.speed, vec_y / side * self.speed))

    def die(self):
        EXP(self, "exp")
        monster_list.remove(self)
        object_list.remove(self)


# 경험치
class EXP(Object):
    def __init__(self, monster, path):
        super().__init__((monster.x, monster.y), path)
        self.player = monster.player
        self.exp_amount = monster.max_hp
        self.speed = 10
        exp_list.append(self)

    def expmove(self):
        vec_x = self.player.x - self.x
        vec_y = self.player.y - self.y
        side = math.sqrt(vec_y ** 2 + vec_x ** 2)
        if side <= 100:
            super().move(
                (vec_x / side * (self.speed - 5), vec_y / side * (self.speed - 5)))


class Weapon(Player):
    pass


class Bullet(Object):
    def __init__(self, maker_pos, path):
        super().__init__(maker_pos, path)


class Background(Object):
    def __init__(self, initial_pos, path):
        super().__init__(initial_pos, path)
        background_list.append(self)

    def check(self):
        if self.x >= screen_width * 2:
            self.x = screen_width * -1
        if self.x <= screen_width * -2:
            self.x = screen_width * 1
        if self.y >= screen_height * 2:
            self.y = screen_height * -1
        if self.y <= screen_height * -2:
            self.y = screen_height * 1
