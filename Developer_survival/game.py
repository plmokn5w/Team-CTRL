from library import *

# 세팅

pygame.init()
pygame.display.set_caption("Developer Survival")
screen = pygame.display.set_mode((screen_width, screen_height))
start_background=pygame.transform.scale(pygame.image.load(os.path.join(current_path,"images\start_background.png")),(screen_width, screen_height))

title = pygame.display.set_mode((screen_width, screen_height))


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


clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()
game_font = pygame.font.Font(None, 20)

monster_count = 0
monster_summon = 100
monster_max = 50

# 배경 생성
for i in range(9):
    Background((((-1+(i % 3)*2)*screen_width / 2), (3-(i//3)*2) * screen_height / 2), "game background")
player = Player("character_scientist", 20, 10)
player.player()
player.weapons.append(Weapon(player, "weapon_cpp", 0.1, 2, 30))


running = player.running

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


#화면 일시정지
stop_flag = False

#선택지 만듦
choice = False
for i in range(1, 6):
    enforce_option_list.append(Option("enforce_option" + str(i)))

#마우스 위치
m_pos = (0,0)

while running:
    print(len(monster_bullet_list))
    dt = clock.tick(30)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            m_pos = pygame.mouse.get_pos()
            if (100 < m_pos[0] < 400 or 500 < m_pos[0] < 800 or 900 < m_pos[0] < 1200) and \
                    150 < m_pos[1] < 550:
                choice = True

        if stop_flag:
            to_x = 0
            to_y = 0
            break

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

    if stop_flag:
        if choice:
            for i in range(3):
                if 100 + i * 400 < m_pos[0] < 400 + i * 400:
                    enforce_option_list[i].enforce(player)
            choice = False
            stop_flag = False
        else:
            continue

    for weapon in player.weapons:
        weapon.shotBullet()

    for bullet in player_bullet_list:
        bullet.move()
        for monster in monster_list:
            if bullet.collide(monster):
                monster.die(bullet.dmg)
                player_bullet_list.remove(bullet)
                break

    for monster in monster_list:
        if type(monster) == range_out_body:
            continue
        monster.move()
        if monster.collide(player):
            player.die(monster.hp)
            monster.die(monster.hp)
            if player.hp <= 0:
                print(monster_bullet.rect, player.rect)
                game_result = "Monster Collision"
                running = False
            # monster.die()
            # game_result = "Monster Collision"
            # running = False
    for monster_bullet in monster_bullet_list:
        monster_bullet.move()
        if monster_bullet.collide(player):
            player.die(monster_bullet.dmg)
            if player.hp <= 0:
                print(monster_bullet.rect, player.rect)
                game_result = "Monster Collision"
                running = False
            else:
                monster_bullet_list.remove(monster_bullet)
    for exp in exp_list:
        exp.move()
        if exp.collide(player):
            if exp.heart:
                player.hp += exp.heartheal
                if player.hp > player.max_hp:
                    player.hp = player.max_hp
            if player.gainEXP(exp):
                stop_flag = True
                random.shuffle(enforce_option_list)
                i = 0
                for option in enforce_option_list:
                    screen.blit(option.img, (100 + i * 400, 150))
                    i += 1
                    pygame.display.update()
    if stop_flag:
        continue
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
        screen.blit(monster_bullet.img, (monster_bullet.x, monster_bullet.y))
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
    player_hp = game_font.render("HP : {} / {}".format(player.hp,player.max_hp), True, (255, 255, 235))
    screen.blit(player_hp, (10, 40))

    # 몬스터 생성 주기
    monster_count += 1

    if monster_count == monster_summon:
        mnum_count = len(monster_list)
        if mnum_count <= player.lv * 15:
            degree = random.randint(1, 360)
            zero_division((player.x + math.cos(degree) * 1000, player.y + math.sin(degree) * 600), player)
            for i in range(10):
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
