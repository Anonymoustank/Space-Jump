
def main():
    import pygame as pg
    from random import randint, choice
    GREEN = (20, 255, 140)
    GREY = (210, 210 ,210)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    PURPLE = (255, 0, 255)
    BLACK = (0, 0, 0)

    pg.init()
    WIDTH = 500
    HEIGHT = 500
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Space Jump")

    myfont = pg.font.SysFont('verdana', 25)

    running = True

    class Background(pg.sprite.Sprite):
        def __init__(self, image_file, location):
            pg.sprite.Sprite.__init__(self)  #call Sprite initializer
            self.image = pg.image.load(image_file)
            self.rect = self.image.get_rect()
            self.rect.left, self.rect.top = location
    
    class Player(pg.sprite.Sprite):
        def __init__(self, color, width, height):
            super().__init__()
            
            self.image = pg.Surface([width, height])
            self.image.fill(WHITE)
            self.image.set_colorkey(WHITE)
    
            # Draw the player (a rectangle)
            pg.draw.rect(self.image, color, [0, 0, width, height])
        
    
            # Fetch the rectangle object that has the dimensions of the image.
            self.rect = self.image.get_rect()
            self.rect.center = (int(width/2), int(height/2))

    high_score = 0
    score = 0

    block_group_list = []

    player = Player(GREEN, 25, 25)
    player.rect.x = 225
    player.rect.y = 250

    block_list = pg.sprite.Group()

    moving_block_list = [None, None, None, None, None, None, None]

    for i in range(1, 6):
        exec("enemy_%s = Player(PURPLE, 25, 5)" % i)
        exec("enemy_%s_speed = 0" % i, globals())
        if i != 1:
            exec("enemy_%s.rect.x = randint(0, 450)" % i)
        else:
            exec("enemy_%s.rect.x = 225" % i)
        exec("enemy_%s.rect.y = 600 - (%s * 150)" %(i, i))
        exec("block_list.add(enemy_%s)" % i)
        exec("block_group_list.append(enemy_%s)" % i)

    jump_block = Player(GREEN, 25, 5) #trampoline block
    jump_block.rect.x = -200
    jump_block.rect.y = 100
    block_list.add(jump_block)
    block_group_list.append(jump_block)

    death_block = Player(RED, 25, 5) #lava block, kills you instantly
    death_block.rect.x = -200
    death_block.rect.y = 150
    block_list.add(death_block)
    block_group_list.append(death_block)

    ref = Player(GREEN, 25, 5) #reference block for distances jumped and fallen
    ref.rect.x = 700
    ref.rect.y = 100
    block_list.add(ref)
    block_group_list.append(ref)

    sprite_list = pg.sprite.Group()

    falling = False

    jumping = False

    sprite_list.add(player)

    clock = pg.time.Clock()

    fps = 60

    screen.fill(BLACK)

    dest_y = ref.rect.y

    BackGround = Background('space.jpg', [0,0])

    tab_exit = False #checks to see if the player exited the while loop by dying or hitting the exit button

    can_move = False #ensures that the player can't move before hitting the first platform
    
    fall_y = ref.rect.y

    jump_in_screen = False #checks if the trampoline is on screen

    death_in_screen = False #checks if death block is on screen

    super_jump = False #checks to see if trampoline block has been hit

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                tab_exit = True
        keys = pg.key.get_pressed()

        if keys[pg.K_r]:
            main()
            
        on_ground = False

        for a, i in enumerate(block_group_list):
            if abs(player.rect.x - i.rect.x) <= 30 and abs(player.rect.bottom - i.rect.top) <= 5 and falling == True and jumping == False and i != ref and i != jump_block and i != death_block:
                can_move = True
                falling = False
                fall_y = ref.rect.y
                if randint(1,10) == 1 and jump_in_screen == False:
                    jump_block.rect.x = randint(0, 450)
                    jump_block.rect.y = -50
                    jump_in_screen = True
                    global enemy_6_speed
                    if randint(1, 2) == 1:
                        enemy_6_speed = -4
                    else:
                        enemy_6_speed = 4
                if randint(1,10) == 1 and death_in_screen == False:
                    death_block.rect.x = randint(0, 450)
                    death_block.rect.y = -50
                    death_in_screen = True
                    global enemy_7_speed
                    if randint(1, 2) == 1:
                        enemy_7_speed = -4
                    else:
                        enemy_7_speed = 4
                if ref.rect.y == dest_y:
                    jumping = False
                if randint(3, 6) != 5:
                    i.rect.y = i.rect.y - 500
                    i.rect.x = randint(0, 450)
                    if i in moving_block_list:
                        moving_block_list[a] = None
                        exec("enemy_%s_speed = 0" % (a + 1), globals())
                else:
                    i.rect.y = i.rect.y - 500
                    i.rect.x = randint(100, 350)
                    if i in moving_block_list:
                        moving_block_list[a] = None
                    if randint(1, 2) == 1:
                        moving_block_list[a] = i
                        exec("enemy_%s_speed = -4" % (a + 1), globals())
                    else:
                        moving_block_list[a] = i
                        exec("enemy_%s_speed = 4" % (a + 1), globals())

                dest_y = ref.rect.y + 360
                if jumping == False and falling == False:
                    jumping = True
                on_ground = True
                break
            else:
                if on_ground == False:
                    falling = True

            if i == jump_block and jump_in_screen == True:
                moving_block_list[a] = i

            if i == death_block and death_in_screen == True:
                moving_block_list[a] = i

            if i == death_block and abs(player.rect.x - i.rect.x) <= 30 and abs(player.rect.y - i.rect.y) <= 30 and super_jump == False:
                running = False
                tab_exit = False

            if i == jump_block and abs(player.rect.x - i.rect.x) <= 30 and abs(player.rect.bottom - i.rect.top) <= 5 and falling == True and jumping == False and i != ref:
                can_move = True
                super_jump = True
                moving_block_list[a] = None
                exec("enemy_%s_speed = 0" % (a + 1), globals())
                falling = False
                jump_in_screen = False
                fall_y = ref.rect.y
                if ref.rect.y == dest_y:
                    jumping = False
                dest_y = ref.rect.y + 1080
                i.rect.x = -300
                if jumping == False and falling == False:
                    jumping = True
                on_ground = True
                break

            if i.rect.y > HEIGHT - 10 and i != ref and i != jump_block and i != death_block:
                if randint(3, 6) != 5:
                    i.rect.y = i.rect.y - 500
                    i.rect.x = randint(0, 450)
                    if i in moving_block_list:
                        moving_block_list[a] = None
                        exec("enemy_%s_speed = 0" % (a + 1), globals())
                else:
                    i.rect.y = i.rect.y - 500
                    i.rect.x = randint(100, 350)
                    if i in moving_block_list:
                        moving_block_list[a] = None
                    if randint(1, 2) == 1:
                        moving_block_list[a] = i
                        exec("enemy_%s_speed = -4" % (a + 1), globals())
                    else:
                        moving_block_list[a] = i
                        exec("enemy_%s_speed = 4" % (a + 1), globals())

            elif i.rect.y > HEIGHT - 10 and i != ref and i == jump_block:
                i.rect.x = -300
                moving_block_list[a] = None
                jump_in_screen = False

            elif i.rect.y > HEIGHT - 10 and i == death_block:
                i.rect.x = -200
                moving_block_list[a] = None
                death_in_screen = False
        
        
        for a, i in enumerate(moving_block_list):
            if i != ref and i != None:
                if i.rect.x >= 485:
                    exec("enemy_%s_speed = -4" % (a + 1), globals())
                elif i.rect.x <= 25:
                    exec("enemy_%s_speed = 4" % (a + 1), globals())
                exec("speed = enemy_%s_speed" % (a + 1), globals())
                i.rect.x += speed

        if falling == True and jumping == False:
            if abs(ref.rect.y - fall_y) < 10:
                for i in block_group_list:
                    i.rect.y -= 1
                    dest_y = ref.rect.y
                score -= 1
            elif abs(ref.rect.y - fall_y) < 60:
                for i in block_group_list:
                    i.rect.y -= 2
                    dest_y = ref.rect.y
                score -= 2
            elif abs(ref.rect.y - fall_y) < 90:
                for i in block_group_list:
                    i.rect.y -= 3
                    dest_y = ref.rect.y
                score -= 3
            else:
                for i in block_group_list:
                    i.rect.y -= 4
                    dest_y = ref.rect.y
                score -= 4

        if len(block_group_list) != 0:
            if ref.rect.y != dest_y:
                fall_y = dest_y
                if abs(ref.rect.y - dest_y) >= 960:
                    for i in block_group_list:
                        i.rect.y += 6
                    score += 6
                if abs(ref.rect.y - dest_y) >= 480:
                    for i in block_group_list:
                        i.rect.y += 5
                    score += 5
                if abs(ref.rect.y - dest_y) >= 400:
                    for i in block_group_list:
                        i.rect.y += 4
                    score += 4
                if abs(ref.rect.y - dest_y) >= 120:
                    for i in block_group_list:
                        i.rect.y += 3
                    score += 3
                elif abs(ref.rect.y - dest_y) >= 20:
                    for i in block_group_list:
                        i.rect.y += 2
                    score += 2
                else:
                    for i in block_group_list:
                        i.rect.y += 1
                    score += 1
            else:
                jumping = False
                super_jump = False
        else:
            if jumping == False:
                running = False
        
        if score > high_score:
            high_score = score
        

        if abs(score - high_score) > 500:
            running = False
            break

        screen.fill(BLACK)
        screen.blit(BackGround.image, BackGround.rect)

        sprite_list.draw(screen)
        block_list.draw(screen)

        textsurface = myfont.render(str(high_score), True, (WHITE))
        screen.blit(textsurface,(0,0))

        if can_move == True:
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                player.rect.x -= 8
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                player.rect.x += 8

        if player.rect.left > WIDTH:
            player.rect.right = 0
        if player.rect.right < 0:
            player.rect.left = WIDTH

        block_list.update()
        sprite_list.update()

        screen.fill(BLACK)
        screen.blit(BackGround.image, BackGround.rect)

        sprite_list.draw(screen)
        block_list.draw(screen)

        textsurface = myfont.render(str(high_score), True, (WHITE))
        screen.blit(textsurface,(0,0))

        pg.display.update()

        clock.tick(fps)
    if tab_exit == False:
        while player.rect.y < HEIGHT:
            player.rect.y +=2
            screen.fill(BLACK)
            screen.blit(BackGround.image, BackGround.rect)
            sprite_list.draw(screen)
            block_list.draw(screen)
            pg.display.update()

        screen.fill(BLACK)
        textsurface = myfont.render("Final Score: " + str(high_score), True, (WHITE))
        screen.blit(textsurface, (150, 200))
        restart_prompt = myfont.render("Press r to restart", True, (WHITE))
        screen.blit(restart_prompt, (145, 300))
        pg.display.update()
        running = True
        while running:
            keys = pg.key.get_pressed()
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    running=False
            if keys[pg.K_r]:
                main()
    pg.quit()
main()