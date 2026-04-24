import pygame
import character


def get_image(sheet, frame, width, height, scale, colour):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet,(0,0),(frame * width, 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colour)
    return image


def check_inside_screen(character,screen_width,screen_height):
    if character.x < 0:
        character.x = 0
        return False
    elif character.x > screen_width - character.width:
        character.x = screen_width - character.width
        return False
    elif character.y < 0:
        character.y = 0
        return False
    elif character.y > screen_height - character.height:
        character.y = screen_height - character.height
        return False
    else:
        return True


def draw_centered_text_over_rect(surface, rendered_text, rect):
    rendered_text_rect = rendered_text.get_rect(center = (rect.centerx,rect.centery))
    surface.blit(rendered_text,rendered_text_rect)


GRAPHICS_PATH = "./Assets/"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
START_POS = (0,0)
BG_COLOUR = (25,175,75)

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("PyGame Red Hood")

font_object = pygame.font.Font(GRAPHICS_PATH + "Swansea-q3pd.ttf", 24)


player_image_sheet = pygame.image.load(GRAPHICS_PATH + "red-riding-hood_1.png")
player_image = get_image(player_image_sheet,0,32,32,1.5,"black")
player = character.Player("Red_hood",player_image,5,[],0,3)
player.x,player.y = START_POS
text_lives = font_object.render(f"Lives: {player.numlives}", True, "black")



enemy1_image_sheet = pygame.image.load(GRAPHICS_PATH + "Shoom_Idle.png")
enemy1_image = get_image(enemy1_image_sheet, 0, 48, 48, 1, (115,135,123))
enemy1 = character.Enemy("Enemy1",enemy1_image,4,(0,400),"H")

enemy2_image_sheet = pygame.image.load(GRAPHICS_PATH + "Dude_Monster_Idle_4.png")
enemy2_image = get_image(enemy2_image_sheet, 0, 32, 32, 1.5, (0,0,0))
enemy2 = character.Enemy("Enemy2",enemy2_image,4,(200,0),"V")
enemies = [enemy1,enemy2]


running = True

while running:
    screen.fill(BG_COLOUR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player.speed
    if keys[pygame.K_RIGHT]:
        player.x += player.speed
    if keys[pygame.K_UP]:
        player.y -= player.speed
    if keys[pygame.K_DOWN]:
        player.y += player.speed
    
    check_inside_screen(player,SCREEN_WIDTH,SCREEN_HEIGHT)
    player_rect = player.draw(screen)
   

    for enemy in enemies:
        enemy.move()
        if check_inside_screen(enemy,SCREEN_WIDTH,SCREEN_HEIGHT) == False:
            enemy.speed = -enemy.speed
        enemy_rect=enemy.draw(screen)
        if player_rect.colliderect(enemy_rect):
            player.numlives -=1
            text_lives = font_object.render(f"Lives: {player.numlives}", True, "black")
            if player.numlives == 0:
                game_over_rect = pygame.draw.rect(screen,"cyan",(300,250,200,100))
                text_game_over = font_object.render("GAME OVER!", True, "black")
                draw_centered_text_over_rect(screen,text_game_over,game_over_rect)
                pygame.display.flip()
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
            player.x,player.y = START_POS

    
    screen.blit(text_lives, (20,SCREEN_HEIGHT-30))
    clock.tick(40)
    pygame.display.flip()


pygame.quit()