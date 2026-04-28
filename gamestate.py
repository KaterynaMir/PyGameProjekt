import pygame

import button
import character
import object


class GameState:

    RED_TEXT_COLOUR = (173,9,33)
    BUTTON_COLOUR = (44,104,76)
    HOVERED_COLOUR = (93,171,180)
    Score = 0

    def __init__(self,screen_width,screen_height,panel_height):
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.PANEL_HEIGHT = panel_height
        self.font1 = pygame.font.Font("./Assets/Swansea-q3pd.ttf", 32)
        self.font2 = pygame.font.Font("./Assets/Block_Stock.ttf", 28)
        self.font2_big = pygame.font.Font("./Assets/Block_Stock.ttf", 58)    
        
    def handle_events(self,events):
        pass

    def draw(self,screen):
        pass

    @staticmethod
    def draw_horizontally_centered_text(surface, rendered_text, y):
        rect= surface.get_rect()
        rendered_text_rect = rendered_text.get_rect(center = (rect.centerx, y))
        surface.blit(rendered_text,rendered_text_rect)
        return rendered_text_rect


class MainMenu(GameState):

    def __init__(self,screen_width,screen_height,panel_height):
        super().__init__(screen_width,screen_height,panel_height)
        self.bg_image = pygame.image.load("./Assets/main_menu_bg_800_660.jpg")
        self.start_button = button.Button("START GAME",self.font2,self.BUTTON_COLOUR,self.HOVERED_COLOUR,(240,280),300,75,20)
        self.quit_button = button.Button("QUIT GAME",self.font2,self.BUTTON_COLOUR,self.HOVERED_COLOUR,(240,380),300,75,20)

    def handle_events(self, events):
        for event in events:
            if self.start_button.is_pressed(event):
                return "game"
            elif self.quit_button.is_pressed(event):
                return "quit"
        return "main_menu"

    def draw(self,screen):
        screen.blit(self.bg_image, (0, 0))
        text_red = self.font2_big.render("RED HOOD", True, self.RED_TEXT_COLOUR)
        text_black = self.font2_big.render("RED HOOD", True, (0,0,0))
        screen.blit(text_black,(280, 181))
        screen.blit(text_red,(277, 178))
        self.start_button.draw(screen)
        self.quit_button.draw(screen)
        

class GameScreen(GameState):
    START_POS = (0,0)
    BG_COLOUR = (25,175,75)

    def __init__(self,screen_width,screen_height,panel_height,pos=START_POS):
        super().__init__(screen_width,screen_height,panel_height)
        player_image_sheet = pygame.image.load("./Assets/red-riding-hood_1.png")
        player_image = self.get_image(player_image_sheet,0,0,32,32,1.5,(0,0,0))
        self.player = character.Player("Red_hood",player_image,5,3)
        self.player.x,self.player.y = pos

        enemy1_image_sheet = pygame.image.load("./Assets/Shoom_Idle.png")
        enemy1_image = self.get_image(enemy1_image_sheet,0,0,48,48,1,(115,135,123))
        enemy1 = character.Enemy("Enemy1",enemy1_image,4,(0,400),"H")

        enemy2_image_sheet = pygame.image.load("./Assets/Dude_Monster_Idle_4.png")
        enemy2_image = self.get_image(enemy2_image_sheet,0,0,32,32,1.5,(0,0,0))
        enemy2 = character.Enemy("Enemy2",enemy2_image,4,(200,0),"V")
        self.enemies = [enemy1,enemy2]

        flower_sheet = pygame.image.load("./Assets/Flowers_With_Outline_SpriteSheet.png")
        flower_list = []
        for j in range(2):
            for i in range(6):
                flower_image = self.get_image(flower_sheet, i, j, 32, 32, 1, (0,0,0))    
                flower_list.append(flower_image)
        self.flowers_group = object.Object.place_random_objects(30,flower_list,self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        
    @staticmethod
    def get_image(sheet,frame_x,frame_y,width,height,scale,colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(sheet,(0,0),(frame_x * width, frame_y * height, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)
        return image

    def check_inside_screen(self,character,screen_width,screen_height):
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

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
               # if event.key == pygame.K_ESCAPE:
                #    return "main_menu"
                if event.key == pygame.K_p:
                    return "pause"
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.x -= self.player.speed
        if keys[pygame.K_RIGHT]:
            self.player.x += self.player.speed
        if keys[pygame.K_UP]:
            self.player.y -= self.player.speed
        if keys[pygame.K_DOWN]:
            self.player.y += self.player.speed
        self.check_inside_screen(self.player,self.SCREEN_WIDTH,self.SCREEN_HEIGHT)
        
        for enemy in self.enemies:
            enemy.move()
            if self.check_inside_screen(enemy,self.SCREEN_WIDTH,self.SCREEN_HEIGHT) == False:
                enemy.speed = -enemy.speed
            if self.player.get_rectangle().colliderect(enemy.get_rectangle()):
                self.player.numlives -=1
                if self.player.numlives == 0:
                    return "game_over"
                else:
                    self.player.x,self.player.y = self.START_POS
        
        for flower in self.flowers_group:
            if self.player.get_rectangle().colliderect(flower):
                GameState.Score += 10
                flower.kill()
        return "game"
    

    def draw(self,screen):
        screen.fill(self.BG_COLOUR)
        pygame.draw.rect(screen,(0,0,0),(0,self.SCREEN_HEIGHT,self.SCREEN_WIDTH,self.PANEL_HEIGHT))
        self.flowers_group.draw(screen)
        self.player.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        text_lives = self.font1.render(f"Lives: {self.player.numlives}", True, (255,255,255))
        screen.blit(text_lives, (20,self.SCREEN_HEIGHT + 15))
        text_score = self.font1.render(f"Score: {GameState.Score}", True, (255,255,255))
        screen.blit(text_score, (620,self.SCREEN_HEIGHT + 15))


class Pause(GameState):

    def __init__(self,screen_width,screen_height,panel_height):
        super().__init__(screen_width,screen_height,panel_height)
        self.bg_image = pygame.image.load("./Assets/paused_bg_800_660.jpg")
        self.menu_button = button.Button("MAIN MENU",self.font2,self.BUTTON_COLOUR,self.HOVERED_COLOUR,(10,200),300,75,20)
        self.continue_button = button.Button("CONTINUE",self.font2,self.BUTTON_COLOUR,self.HOVERED_COLOUR,(490,200),300,75,20)

    def handle_events(self, events):
        for event in events:
            if self.menu_button.is_pressed(event):
                return "main_menu"
            elif self.continue_button.is_pressed(event):
                return "game"
        return "pause"

    def draw(self,screen):
        screen.blit(self.bg_image, (0, 0))
        text_red = self.font2_big.render("GAME PAUSED", True, self.RED_TEXT_COLOUR)
        text_black = self.font2_big.render("GAME PAUSED", True, (0,0,0))
        text_rect = self.draw_horizontally_centered_text(screen, text_black, 130)
        screen.blit(text_red,(text_rect.x - 3, text_rect.y - 3))
        self.menu_button.draw(screen)
        self.continue_button.draw(screen)


class GameOver(GameState):

    def __init__(self,screen_width,screen_height,panel_height):
        super().__init__(screen_width,screen_height,panel_height)
        self.bg_image = pygame.image.load("./Assets/game_over_bg_800_660.jpg")
        self.menu_button = button.Button("MAIN MENU",self.font2,self.BUTTON_COLOUR,self.HOVERED_COLOUR,(410,290),300,75,20)
        self.quit_button = button.Button("QUIT GAME",self.font2,self.BUTTON_COLOUR,self.HOVERED_COLOUR,(410,410),300,75,20)

    def handle_events(self, events):
        for event in events:
            if self.menu_button.is_pressed(event):
                return "main_menu"
            elif self.quit_button.is_pressed(event):
                return "quit"
        return "game_over"

    def draw(self,screen):
        screen.blit(self.bg_image, (0, 0))
        text_red = self.font2_big.render("GAME OVER", True, self.RED_TEXT_COLOUR)
        text_black = self.font2_big.render("GAME OVER", True, (0,0,0))
        text_rect = self.draw_horizontally_centered_text(screen, text_black, 180)
        screen.blit(text_red,(text_rect.x - 3, text_rect.y - 3))
        self.menu_button.draw(screen)
        self.quit_button.draw(screen)
        text_score_red = self.font2.render(f"YOUR SCORE: {GameState.Score}", True, self.RED_TEXT_COLOUR)
        text_score_black = self.font2.render(f"YOUR SCORE: {GameState.Score}", True, (0,0,0))
        text_score_rect = self.draw_horizontally_centered_text(screen, text_score_black, 250)
        screen.blit(text_score_red,(text_score_rect.x - 3, text_score_rect.y - 3))
