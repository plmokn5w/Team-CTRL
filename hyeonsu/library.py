import pygame
import os
import math
import random

# 화면 크기
screen_width = 1280
screen_height = 800
# 파일 경로
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

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

# 추가된 리스트
object_list = []
background_list = []
enforce_option_list = []
##

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
        if self not in object_list:
            object_list.append(self)

    def move(self, to_pos):
        self.x += to_pos[0]
        self.y += to_pos[1]
        self.rect.left = self.x
        self.rect.top = self.y

    def collide(self, obj):
        return self.rect.colliderect(obj.rect)

    def player(self):
        object_list.remove(self)

    def movebackground(self, to_x, to_y):  # 주인공이 움직이면 다른 애들이 그 반대방향으로 움직인다
        self.x -= to_x
        self.y -= to_y
        self.rect.left = self.x
        self.rect.top = self.y


# 플레이어
class Player(Object):
    def __init__(self, character_name,
                 initial_hp, initial_speed):
        super().__init__((screen_width / 2, screen_height / 2), character_name)
        self.lv = 1
        self.max_hp = initial_hp
        self.hp = self.max_hp
        self.speed = initial_speed
        self.to_x = 0
        self.to_y = 0
        self.weapons = []
        self.exp = 0
        self.exp_allot = self.lv * 3

    def gainEXP(self, exp):
        self.exp += exp.exp_amount
        exp_list.remove(exp)
        if self.exp >= self.exp_allot:
            self.exp = 0
            self.levelUp()
            return True
        return False

    def levelUp(self):
        self.lv += 1
        self.exp_allot = self.exp_allot * 2


# 몬스터
monster_name_list = ["zero_division", "stack_overflow", "range_out_head"]


class zero_division(Object):
    def __init__(self, monster_pos, player):
        super().__init__(monster_pos, "zero_division")
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
        self.speed = 4
        self.dmg = 2
        self.shoot_count = 0
        self.shoot_act = 25
        monster_list.append(self)

    def move(self):
        self.shoot_count += 1
        if self.shoot_count >= self.shoot_act:
            self.shoot()
            self.shoot_count = 0
        distance = math.sqrt((self.x - self.player.x) ** 2 + (self.y - self.player.y) ** 2)
        vec_x = self.player.x - self.x
        vec_y = self.player.y - self.y
        side = math.sqrt(vec_y ** 2 + vec_x ** 2)
        if 200 + 3 < distance:
            super().move((vec_x / side * self.speed, vec_y / side * self.speed))
        elif 200 - 3 > distance:
            super().move((vec_x / side * -self.speed, vec_y / side * -self.speed))

    def shoot(self):
        bullet((self.x, self.y), self.player)

    def die(self):
        EXP(self, "exp")
        monster_list.remove(self)


class bullet(Object):
    def __init__(self, monster_pos, player):
        super().__init__(monster_pos, "bullet")
        self.speed = 8
        self.player = player
        self.x = monster_pos[0]
        self.y = monster_pos[1]
        vec_x = player.x - self.x
        vec_y = player.y - self.y
        side = math.sqrt(vec_y ** 2 + vec_x ** 2)
        self.vector = (vec_x / side * self.speed, vec_y / side * self.speed)  # (math.atan2(vec_y,vec_x)*180/math.pi)
        self.img = pygame.transform.rotate(self.img, math.atan(vec_x / vec_y) * 180 / math.pi)
        self.img = pygame.transform.scale(self.img, (15, 45))
        self.rect = self.img.get_rect()
        monster_bullet_list.append(self)

    def move(self):
        if math.sqrt((self.x - self.player.x) ** 2 + (self.y - self.player.y) ** 2) >= 800:
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
        self.speed = 2
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
        self.speed = 6
        self.dmg = 3
        self.body = [range_out_body((self.x, self.y), self, self.player)]
        for i in range(9):
            self.body.append(range_out_body((self.x, self.y), self.body[i], self.player))
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
        # self.img=pygame.transform.rotate(self.img,(vec_x/vec_y))
        for body in self.body:
            body.move(self.speed)

    def paint(self, screen):
        for body in self.body[-1:]:
            screen.blit(body.img, (body.x, body.y))

    def die(self):
        EXP(self, "exp")
        for body in self.body:
            if body in monster_list:
                monster_list.remove(body)
        monster_list.remove(self)

class range_out_body(Object):
    def __init__(self, monster_pos, front, player):
        super().__init__(monster_pos, "range_out")
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
        self.max_hp = 1
        self.player = player
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

    def die(self):
        EXP(self, "exp")
        if self in monster_list:
            monster_list.remove(self)


class Background(Object):
    def __init__(self, initial_pos, path):
        super().__init__(initial_pos, path)
        background_list.append(self)

    def check(self):
        if self.x >= screen_width * 2:
            self.x -= screen_width * 3
        if self.x <= screen_width * -2:
            self.x += screen_width * 3
        if self.y >= screen_height * 2:
            self.y -= screen_height * 3
        if self.y <= screen_height * -2:
            self.y += screen_height * 3


class EXP(Object):
    def __init__(self, monster, path):
        super().__init__((monster.x + monster.width / 2, monster.y + monster.height / 2), path)
        self.player = monster.player
        self.exp_amount = monster.max_hp
        self.speed = 15
        exp_list.append(self)

    def move(self):
        vec_x = self.player.x - self.x
        vec_y = self.player.y - self.y
        side = math.sqrt(vec_y ** 2 + vec_x ** 2)
        if side <= 100:
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
        self.img = pygame.transform.scale(self.img, (int(screen_width * (self.player.exp / self.player.exp_allot)) + 1, 30))
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
        self.bullet_cnt = 1
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
        for i in range(self.bullet_cnt):
            velocity = (velocity[0] + int(velocity[0] * math.cos(i * 15)), 
            velocity[1] + int(velocity[1] * math.sin(i * 15)))
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
    
class Option:
    def __init__(self, path):
        self.name = path
        self.img = pygame.image.load(os.path.join(image_path, self.name + ".png"))
    
    def enforce(self, player):
        if (self.name == "enforce_option1"):
            player.weapons[0].bullet_cnt += 1
        if (self.name == "enforce_option2"):
            player.weapons[0].attack_delay //= 2
        if (self.name == "enforce_option3"):
            player.max_hp *= 2
            player.hp = player.max_hp
        if (self.name == "enforce_option4"):
            player.speed += 2
        if (self.name == "enforce_option5"):
            player.weapon[0].bullet_dmg += 1
        
