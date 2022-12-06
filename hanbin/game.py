from library import *

# 세팅
pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Developer Survival")

clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()
game_font = pygame.font.Font(None, 20)

running = True

# 배경 생성
for i in range(9):
    Background(((-1+(i % 3)*2)*screen_width / 2, (3-(i//3)*2) * screen_height / 2), "game background")

to_x = 0
to_y = 0
player = Player("character_scientist", 100, 6)

for _ in range(5):
    amount = random.randint(150, 200)
    dir = random.choice([-1, 1])
    dx = amount * dir
    amount = random.randint(150, 200)
    dir = random.choice([-1, 1])
    dy = amount * dir
    Monster((player.x + dx, player.y + dy), "zero_division", player)

# 게임
while running:

    dt = clock.tick(30)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= player.speed
            if event.key == pygame.K_RIGHT:
                to_x += player.speed
            if event.key == pygame.K_UP:
                to_y -= player.speed
            if event.key == pygame.K_DOWN:
                to_y += player.speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0
# 모든 player.to_x와 player.to_y를 to_x와 to_y로 교체
    for monster in monster_list:
        monster.notplayer()
        monster.monmove()
        if monster.collide(player):
            monster.die()
            # game_result = "Monster Collision"
            # running = False

    for exp in exp_list:
        exp.notplayer()
        exp.expmove()
        if exp.collide(player):
            player.gain_exp(exp)

    for background in background_list:
        background.notplayer()
        background.check()
    # 배경 무한대로 이어지게 하기
    # 물체들 다 움직이기
    for object in object_list:
        object.movebackground(to_x, to_y)
        screen.blit(object.img, (object.x, object.y))
    #
    screen.blit(player.img, (player.x, player.y))
    for monster in monster_list:
        screen.blit(monster.img, (monster.x, monster.y))
    for exp in exp_list:
        screen.blit(exp.img, (exp.x, exp.y))

    game_font = pygame.font.Font(None, 40)
    weapon_left_text = game_font.render("Level : {}".format(player.lv), True, (255, 255, 235))
    screen.blit(weapon_left_text, (10, 10))

    # 화면 업데이트
    pygame.display.update()

game_font = pygame.font.Font(None, 80)
msg = game_font.render(game_result, True, (255, 255, 235))
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(500)

pygame.quit()
