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

for _ in range(5):
    degree=random.randint(1,360)
    dx=math.cos(degree)*200
    dy=math.sin(degree)*200
    zero_division((player.x + dx, player.y + dy), player)

# 게임
while running:
    print(len(monster_bullet_list))
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

    for monster in monster_list:
        monster.move()
        if monster.collide(player):
            monster.die()
            #game_result = "Monster Collision"
            #running = False
    for monster_bullet in monster_bullet_list:
        monster_bullet.move()
        if monster_bullet.collide(player):
            print(monster_bullet.rect, player.rect)
            game_result = "Monster Collision"
            running = False
    for exp in exp_list:
        exp.move()
        if exp.collide(player):
            player.gain_exp(exp)
    
    screen.blit(background.img, (background.x, background.y))
    screen.blit(player.img, (player.x, player.y))
    for monster in monster_list:
        screen.blit(monster.img, (monster.x, monster.y))
    for monster_bullet in monster_bullet_list:
        screen.blit(monster_bullet.img,(monster_bullet.x,monster_bullet.y))
    for exp in exp_list:
        screen.blit(exp.img, (exp.x, exp.y))

    game_font = pygame.font.Font(None, 40)
    weapon_left_text = game_font.render("Level : {}".format(player.lv), True, (255, 255, 235))
    screen.blit(weapon_left_text, (10, 10))

    # 화면 업데이트
    pygame.display.update()

game_font = pygame.font.Font(None, 80)
msg = game_font.render(game_result, True, (255, 255, 235))
msg_rect = msg.get_rect(center = (int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(500)

pygame.quit()