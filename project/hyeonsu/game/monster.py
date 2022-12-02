import os
import math
import pygame
current_path = os.path.dirname(__file__)  # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "../project/images4/monster")  # images 폴더 위치 반환
nameset=["zero_division", "stack_overflow", "range_out_head"]
def setmonster(name: str):
    #return [health, speed, damage]
    if name=="zero_division":
        return [1,3,2]
    elif name=="stack_overflow":
        return [10,2,4]
    elif name=="range_out":
        return [5,1,2]

class monster:
    picture=0
    body=0
    pos=[0,0]
    name:str
    stat=[0,0,0]
    hitbox=[0,0]
    before_pos=[]
    #생성자 메서드
    def __init__(self, monster_pos,name):
        self.name=nameset[name]
        self.pos=monster_pos
        self.stat=setmonster(nameset[name])
        self.picture = pygame.transform.scale(pygame.image.load(os.path.join(image_path, nameset[name]+".png")),(100,100))
        if name==2:
            self.body=pygame.image.load(os.path.join(image_path),"range_out")
        self.hitbox=self.picture.get_rect().size

    ##몬스터가 플레이어를 향해 이동
    def toplayer(self, player_pos):
        vec_x = player_pos[0] - self.pos[0]
        vec_y = player_pos[1] - self.pos[1]
        side = math.sqrt(vec_y ** 2 + vec_x ** 2)
        self.pos[0]+=vec_x/side*self.stat[1]
        self.pos[1]+=vec_y/side*self.stat[1]


