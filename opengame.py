import os
import pygame
from time import sleep
from python import monster
##############################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init()

# 화면 크기 설정
screen_width = 800  # 가로 크기
screen_height = 500  # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Developer servival")

# FPS
clock = pygame.time.Clock()
##############################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__)  # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "images4")  # images 폴더 위치 반환
resource = os.path.join(current_path, "../python")  # 게임 구현에 필요한 리소스 폴더 위치
resource
# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character_scientist.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width - character_width
character_y_pos = screen_height / 2 - character_height / 2

# 캐릭터 이동 방향
character_to_y = 0
character_to_x = 0

# 캐릭터 이동 속도
character_speed = 6
character_x_speed = 6
character_y_speed = 6

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon_c.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
weapon_height = weapon_size[1]

# 무기 한번에 여러발 발사 가능
weapons = []

# 무기 이동속도
weapon_speed = 12
# 무기 탄창
weapon_left = 1000

# 별 만들기
heart = pygame.image.load(os.path.join(image_path, "heart.png"))
heart_size = weapon.get_rect().size
heart_width = weapon_size[0]
heart_height = weapon_size[1]

# 별 여러개 있을 수 있음
hearts = []

# 몬스터 만들기
monsters=[]
Monster= monster.monster([100,100],0)
monsters.append(Monster)

# 공 이동 방향
ball_to_x = 3
ball_to_y = 0
# 공 이동 속도
ball_init_speed = 6

# 폰트 지정
game_font = pygame.font.Font(None, 20)
# 시간 지정
start_ticks = pygame.time.get_ticks()  # 시작 시간 정의

# 게임 종료 메시지
# time out
# mission complete
# game over
game_result = "Game over"

running = True

while running:
    dt = clock.tick(61)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # 사용자 입력 받기
        # 키가 눌렸을 때
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x = -character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x = character_speed
            if event.key == pygame.K_UP:
                character_to_y = -character_speed
            elif event.key == pygame.K_DOWN:
                character_to_y = character_speed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                character_to_y = 0
        # 키가 때어 졌을 때

    # 3. 게임 캐릭터 위치 정의
    for i in range(10):
        character_y_pos += character_to_y / 10
        character_x_pos += character_to_x / 10
        sleep(0.001)
    character_rect = character.get_rect()#캐릭터 쿨라이더 지정
    character_rect.center=[character_x_pos,character_y_pos]
    # 무기 위치 조정
    weapons = [[w[0] - weapon_speed, w[1]] for w in weapons]  # 발판 위치 옆으로 이동하기

    #몬스터 위치 조정
    for mon in monsters:
        mon.toplayer([character_x_pos,character_y_pos])
        monster_rect=mon.picture.get_rect()
        monster_rect.center=mon.pos

        if (monster_rect.colliderect(character_rect)):
            print(monster_rect, character_rect)
            game_result = "game over"
            running = False

    for weapon_idx, weapon_val in enumerate(weapons):
        weapon_pos_x = weapon_val[0]
        weapon_pos_y = weapon_val[1]

        # 무기 rect 정보 업데이트
        weapon_rect = weapon.get_rect()
        weapon_rect.left = weapon_pos_x
        weapon_rect.top = weapon_pos_y

        # 충돌 체크
        #if weapon_rect.colliderect(heart_rect):
        #    game_result = "stage clear"
        #    running = False

    # 하트 추가하기
    hearts = [(10, 350)]
    heart_left = len(hearts)
    heart_rect = heart.get_rect()
    for heart_x_pos, heart_y_pos in hearts:
        heart_rect.left = heart_x_pos
        heart_rect.top = heart_y_pos

        # 충돌 체크


    # 시간 계산
    elapsed_time = pygame.time.get_ticks()/26

    timer = game_font.render("Time : {}".format(int(elapsed_time/1000)), True, (255, 255, 235))

    if int(elapsed_time) % 34 == 0:
        weapon_x_pos = character_x_pos
        weapon_y_pos = character_y_pos + character_height / 2 - weapon_height / 2
        weapons.append([weapon_x_pos, weapon_y_pos])



    # 좌표 테스트
    #X = game_font.render("X : {}".format(int(ball_x_pos)), True, (255, 255, 235))
    #Y = game_font.render("Y : {}".format(int(ball_y_pos)), True, (255, 255, 235))
    TO_X = game_font.render("TO_X : {}".format(int(ball_to_x)), True, (255, 255, 235))
    TO_Y = game_font.render("TO_Y : {}".format(int(ball_to_y)), True, (255, 255, 235))

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    # 레벨 그리는 곳
    for heart_x_pos, heart_y_pos in hearts:
        screen.blit(heart, (heart_x_pos, heart_y_pos))

    # 몬스터 그리는 곳
    for mon in monsters:
        screen.blit(mon.picture,mon.pos)
    ######
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(timer, (10, 10))

    # 테스트
    game_font = pygame.font.Font(None, 40)
    weapon_left_text = game_font.render("weapon_left : {}".format(int(weapon_left)), True, (255, 255, 235))
    screen.blit(weapon_left_text, (10, 30))

    pygame.display.update()
# 게임 오버 상황들
game_font = pygame.font.Font(None, 80)
msg = game_font.render(game_result, True, (255, 255, 235))
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(2000)

pygame.quit()
