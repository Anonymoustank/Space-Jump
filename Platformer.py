
def main():

    import pygame as pg
    from random import randint
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
    pg.display.set_caption("Game")

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
    enemy = Player(PURPLE, 25, 5)
    enemy.rect.x = 225
    enemy.rect.y = 400

    player.rect.x = 225
    player.rect.y = 250

    enemy_1 = Player(PURPLE, 25, 5)
    enemy_1.rect.x = 290
    enemy_1.rect.y = 100

    block_list = pg.sprite.Group()
    block_list.add(enemy)
    block_list.add(enemy_1)

    block_group_list.append(enemy)
    block_group_list.append(enemy_1)

    ref = Player(GREEN, 25, 5)
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

    highest_num = 0

    tab_exit = False #checks to see if the player exited the while loop by dying or hitting the exit button

    can_move = False #ensures that the player can't move before hitting the first platform

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                tab_exit = True
        keys = pg.key.get_pressed()
        on_ground = False
        for i in block_group_list:
            if abs(player.rect.x - i.rect.x) <= 20 and abs(player.rect.y - i.rect.y) <= 25:
                can_move = True
                falling = False
                if ref.rect.y == dest_y:
                    jumping = False
                for a in block_group_list:
                    if a.rect.y > highest_num:
                        highest_num = a.rect.y
                i.rect.y = highest_num - 240
                i.rect.x = randint(0, 450)
                dest_y = ref.rect.y + 360
                if jumping == False and falling == False:
                    jumping = True
                on_ground = True
                break
            else:
                if on_ground == False:
                    falling = True
        screen.fill(BLACK)
        screen.blit(BackGround.image, BackGround.rect)

        sprite_list.draw(screen)
        block_list.draw(screen)
        
        if falling == True and jumping == False:
            for i in block_group_list:
                i.rect.y -= 4
                dest_y = ref.rect.y
            score -= 4
            

        if len(block_group_list) != 0:
            if ref.rect.y != dest_y:
                if abs(ref.rect.y - dest_y) >= 120:
                    for i in block_group_list:
                        i.rect.y += 4
                    score += 4
                elif abs(ref.rect.y - dest_y) >= 60:
                    for i in block_group_list:
                        i.rect.y += 3
                    score += 3
                elif abs(ref.rect.y - dest_y) >= 28:
                    for i in block_group_list:
                        i.rect.y += 2
                    score += 2
                else:
                    for i in block_group_list:
                        i.rect.y += 1
                    score += 1
            else:
                jumping = False
        else:
            if jumping == False:
                running = False
        
        if score > high_score:
            high_score = score

        if abs(score - high_score) > 300:
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
                player.rect.x -= 10
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                player.rect.x += 10

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