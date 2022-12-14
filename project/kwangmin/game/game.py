from library import *
# 세팅
pygame.init()
pygame.display.set_caption("Developer Survival")
title = pygame.display.set_mode((screen_width, screen_height))
start_background=pygame.transform.scale(pygame.image.load(os.path.join(current_path,"images\start_background.png")),(screen_width, screen_height))

starter=True
dictionary=True
select=True
while starter:#타이틀
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and select:
                select=False
            elif event.key == pygame.K_UP and not select:
                select=True
            elif event.key == pygame.K_SPACE:
                if select:
                    dictionary=False
                    starter=False
                else:
                    starter=False
    pygame.time.delay(100)
    title.blit(start_background,(0,0))
    if select:
        pygame.draw.rect(title, (255, 255, 255), (473, 431, 281, 113), 1)
    else:
        pygame.draw.rect(title, (255, 255, 255), (473, 568, 281, 121), 1)
    pygame.display.update()
Dict=[pygame.image.load(os.path.join(current_path,"images\zero_dict.png")), pygame.image.load(os.path.join(current_path,"images\stack_dict.png")), pygame.image.load(os.path.join(current_path,"images\\range_dict.png"))]
index=0
while dictionary:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                index-=1
                if index<0:
                    index=2
            elif event.key == pygame.K_RIGHT:
                index+=1
                if index>=3:
                    index=0
            elif event.key == pygame.K_SPACE:
                dictionary=False
        pygame.time.delay(100)
        title.blit(Dict[index], (0, 0))
        pygame.display.update()

screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()
game_font = pygame.font.Font(None, 20)

monster_count = 0
monster_summon = 50



running = True

# 배경 생성
for i in range(9):
    Background((((-1+(i % 3)*2)*screen_width / 2), (3-(i//3)*2) * screen_height / 2), "game background")
player = Player("character_scientist", 100, 10)
player.player()
player.weapons.append(Weapon(player, "weapon_cpp", 0.1, 8, 45))

# test
degree = random.randint(1, 360)
zero_division((player.x + math.cos(degree) * 900, player.y + math.sin(degree) * 600), player)
for i in range(2):

    degree = random.randint(1, 360)
    stack_overflow((player.x + math.cos(degree) * 900, player.y + math.sin(degree) * 600), player)
    degree = random.randint(1, 360)
    range_out((player.x + math.cos(degree) * 900, player.y + math.sin(degree) * 600), player)

exp_bar = EXPBar(player, "exp_bar")

to_x = 0
to_y = 0
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

    for weapon in player.weapons:
        weapon.shotBullet()

    for bullet in player_bullet_list:
        bullet.move()
        for monster in monster_list:
            if bullet.collide(monster):
                monster.die()
                player_bullet_list.remove(bullet)
                break

    for monster in monster_list:
        if type(monster) == range_out_body:
            continue
        monster.move()
        if monster.collide(player):
            monster.die()
            # game_result = "Monster Collision"
            # running = False
    for monster_bullet in monster_bullet_list:
        monster_bullet.move()
        if monster_bullet.collide(player):
            game_result = "Monster Collision"
            running = False
    for exp in exp_list:
        exp.move()
        if exp.collide(player):
            player.gainEXP(exp)

    exp_bar.resize()

    for background in background_list:
        background.check()
    for object in object_list:
        object.movebackground(to_x, to_y)

    # 그리기
    for background in background_list:
        screen.blit(background.img,(background.x, background.y))
    screen.blit(player.img, (player.x, player.y))
    for monster in monster_list:
        if type(monster) == range_out:
            monster.paint(screen)
        screen.blit(monster.img, (monster.x, monster.y))
    for monster_bullet in monster_bullet_list:
        screen.blit(monster_bullet.rotated_image, (monster_bullet.x + monster_bullet.img.get_width() / 2 - monster_bullet.rotated_image.get_width() / 2,monster_bullet.y + monster_bullet.img.get_height() / 2 - monster_bullet.rotated_image.get_height() / 2))


    for bullet in player_bullet_list:
        screen.blit(bullet.img, (bullet.x, bullet.y))
    for exp in exp_list:
        screen.blit(exp.img, (exp.x, exp.y))
    screen.blit(exp_bar.img, (0, 0))
    # 배경 무한대로 이어지게 하기
    # 물체들 다 움직이기

    #
    game_font = pygame.font.Font(None, 40)
    weapon_left_text = game_font.render("Level : {}".format(player.lv), True, (255, 255, 235))
    screen.blit(weapon_left_text, (10, 10))

    # 몬스터 생성 주기
    monster_count += 1

    if monster_count == monster_summon:
        degree = random.randint(1, 360)
        zero_division((player.x + math.cos(degree) * 1000, player.y + math.sin(degree) * 600), player)
        for i in range(2):

            degree = random.randint(1, 360)
            stack_overflow((player.x + math.cos(degree) * 900, player.y + math.sin(degree) * 600), player)
            degree = random.randint(1, 360)
            range_out((player.x + math.cos(degree) * 1100, player.y + math.sin(degree) * 600), player)
        monster_count = 0
    # 화면 업데이트
    pygame.display.update()

game_font = pygame.font.Font(None, 80)
msg = game_font.render(game_result, True, (255, 255, 235))
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(500)

pygame.quit()
