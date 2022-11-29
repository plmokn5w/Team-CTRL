import os
import pygame
from time import sleep

##############################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init()

# 화면 크기 설정
screen_width = 500  # 가로 크기
screen_height = 800  # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Nado Pang")

# FPS
clock = pygame.time.Clock()
##############################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__)  # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "images3")  # images 폴더 위치 반환

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width - character_width
character_y_pos = screen_height/2 - character_height/2

# 캐릭터 이동 방향
character_to_y = 0

# 캐릭터 이동 속도
character_speed = 6

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
weapon_height = weapon_size[1]

# 무기 한번에 여라발 발사 가능
weapons = []

# 무기 이동속도
weapon_speed = 6
# 무기 탄창
weapon_left = 10

# 별 만들기
heart = pygame.image.load(os.path.join(image_path, "heart.png"))
heart_size = weapon.get_rect().size
heart_width = weapon_size[0]
heart_height = weapon_size[1]

# 별 여러개 있을 수 있음
hearts = []


# 공 만들기
ball = pygame.image.load(os.path.join(image_path, "ball.png"))
ball_size = ball.get_rect().size
ball_width = ball_size[0]
ball_height = ball_size[1]
ball_x_pos = (screen_width / 2) - (ball_width / 2)
ball_y_pos = ball_height / 2

# 공 이동 방향
ball_to_x = 3
ball_to_y = 0
# 공 이동 속도
ball_init_speed = -11

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
    dt = clock.tick(30)
    
    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # 사용자 입력 받기
        # 키가 눌렸을 때
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_y -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_y += character_speed
            elif event.key == pygame.K_SPACE:
                if weapon_left > 0:
                    weapon_x_pos = character_x_pos
                    weapon_y_pos = character_y_pos + character_height /2 - weapon_height /2
                    weapons.append([weapon_x_pos, weapon_y_pos])
                    weapon_left -= 1
        # 키가 때어 졌을 때
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_y = 0
    # 3. 게임 캐릭터 위치 정의
    for i in range(10):
        character_y_pos += character_to_y / 10
        sleep(0.001)

    # 무기 위치 조정
    weapons = [[w[0] - weapon_speed, w[1]] for w in weapons]  # 발판 위치 옆으로 이동하기

    # 공 위치 정하기

    if ball_x_pos < 0 or ball_x_pos > screen_width - ball_width:
        ball_to_x = ball_to_x * -1
    if ball_y_pos > screen_height:
        game_result = "Game Over"
        running = False

    # 중력
    ball_to_y += 0.3

    ball_x_pos += ball_to_x
    ball_y_pos += ball_to_y
    # 4. 충돌 처리
    ball_rect = ball.get_rect()
    ball_rect.left = ball_x_pos
    ball_rect.top = ball_y_pos

    for weapon_idx, weapon_val in enumerate(weapons):
        weapon_pos_x = weapon_val[0]
        weapon_pos_y = weapon_val[1]

        # 무기 rect 정보 업데이트
        weapon_rect = weapon.get_rect()
        weapon_rect.left = weapon_pos_x
        weapon_rect.top = weapon_pos_y

        # 충돌 체크
        if weapon_rect.colliderect(ball_rect):
            ball_to_y = ball_init_speed

    # 하트 추가하기
    hearts = [(10, 300)]
    heart_left = len(hearts)
    heart_rect = heart.get_rect()
    for heart_x_pos, heart_y_pos in hearts:
        heart_rect.left = heart_x_pos
        heart_rect.top = heart_y_pos

        # 충돌 체크
        if heart_rect.colliderect(ball_rect):
            game_result = "Stage Clear!"
            running = False
    # 시간 계산
    elapsed_time = pygame.time.get_ticks() / 1000
    timer = game_font.render("Time : {}".format(int(elapsed_time)), True, (255, 255, 235))

    # 좌표 테스트
    X = game_font.render("X : {}".format(int(ball_x_pos)), True, (255, 255, 235))
    Y = game_font.render("Y : {}".format(int(ball_y_pos)), True, (255, 255, 235))
    TO_X = game_font.render("TO_X : {}".format(int(ball_to_x)), True, (255, 255, 235))
    TO_Y = game_font.render("TO_Y : {}".format(int(ball_to_y)), True, (255, 255, 235))

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    # 레벨 그리는 곳
    for heart_x_pos, heart_y_pos in hearts:
        screen.blit(heart, (heart_x_pos, heart_y_pos))

    ######
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(ball, (ball_x_pos, ball_y_pos))
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
