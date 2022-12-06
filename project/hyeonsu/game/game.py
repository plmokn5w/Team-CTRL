from library import *

# 세팅
pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Developer Survival")

clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()
game_font = pygame.font.Font(None, 20)

running = True

background = Object((screen_width / 2, screen_height / 2), "background")
player = Player("character_scientist", 100, 6)
player.weapons.append(Weapon(player, "weapon_cpp", 0.1, 10, 60))

for _ in range(5):
    amount = random.randint(150, 200)
    dir = random.choice([-1, 1])
    dx = amount * dir
    amount = random.randint(150, 200)
    dir = random.choice([-1, 1])
    dy = amount * dir
    Monster((player.x + dx, player.y + dy), "zero_division", player)

exp_bar = EXPBar(player, "exp_bar")

# 게임
while running:

    dt = clock.tick(30)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.to_x -= player.speed
            if event.key == pygame.K_RIGHT:
                player.to_x += player.speed
            if event.key == pygame.K_UP:
                player.to_y -= player.speed
            if event.key == pygame.K_DOWN:
                player.to_y += player.speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.to_x = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player.to_y = 0
        
    player.move()

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
        monster.move()
        if monster.collide(player):
            monster.die()
            #game_result = "Monster Collision"
            #running = False
    
    for exp in exp_list:
        exp.move()
        if exp.collide(player):
            player.gainEXP(exp)
    
    exp_bar.resize()

    w_x = - (player.x + player.width / 2) + screen_width / 2
    w_y = - (player.y + player.height / 2) + screen_height / 2
    
    screen.blit(background.img, (background.x, background.y))
    screen.blit(player.img, (player.x + w_x, player.y + w_y))
    for bullet in player_bullet_list:
        screen.blit(bullet.img, (bullet.x + w_x, bullet.y + w_y))
    for monster in monster_list:
        screen.blit(monster.img, (monster.x + w_x, monster.y + w_y))
    for exp in exp_list:
        screen.blit(exp.img, (exp.x + w_x, exp.y + w_y))
    screen.blit(exp_bar.img, (0, 0))

    game_font = pygame.font.Font(None, 40)
    lv_text = game_font.render("LV : {}".format(player.lv), True, (255, 255, 235))
    screen.blit(lv_text, (10, 60))

    game_font = pygame.font.Font(None, 20)
    exp_text = game_font.render("exp : {}".format(player.exp), True, (255, 255, 235))
    screen.blit(exp_text, (10, 90))

    # 화면 업데이트
    pygame.display.update()

game_font = pygame.font.Font(None, 80)
msg = game_font.render(game_result, True, (255, 255, 235))
msg_rect = msg.get_rect(center = (int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(500)

pygame.quit()