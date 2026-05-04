import pygame

import button
import character
import object
import tileset
import tilemap


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
        self.click_sound =  pygame.mixer.Sound("./Assets/universfield-mouse-click-117076.mp3")
        
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
                self.click_sound.play()
                pygame.time.delay(500)
                return "game"
            elif self.quit_button.is_pressed(event):
                self.click_sound.play()
                pygame.time.delay(500)
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
    WOLF_POS = (750,450)
    BG_COLOUR = (89,193,53)

    def __init__(self,screen_width,screen_height,panel_height,pos=START_POS):
        super().__init__(screen_width,screen_height,panel_height)
        player_image_sheet = pygame.image.load("./Assets/red-riding-hood_1.png")
        player_image = self.get_image(player_image_sheet,0,0,32,32,1.5,(0,0,0))
        self.player = character.Player("Red_hood",player_image,5,pos,3)

        enemy1_image_sheet = pygame.image.load("./Assets/Shoom_Idle.png")
        enemy1_image = self.get_image(enemy1_image_sheet,0,0,48,48,1,(115,135,123))
        enemy1 = character.Enemy("Enemy1",enemy1_image,4,(0,400),"H")
        self.enemies = pygame.sprite.Group()
        self.enemies.add(enemy1)

        enemy2_image_sheet = pygame.image.load("./Assets/Dude_Monster_Idle_4.png")
        enemy2_image = self.get_image(enemy2_image_sheet,0,0,32,32,1.5,(0,0,0))
        enemy2 = character.Enemy("Enemy2",enemy2_image,4,(200,0),"V")
        self.enemies.add(enemy2)

        wolf_image_sheet = pygame.image.load("./Assets/wolf.png")
        wolf_image = self.get_image(wolf_image_sheet,0,0,48,48,1,(255,255,255))
        self.wolf = character.Wolf("Wolf",wolf_image,4,(self.WOLF_POS))
        self.enemies.add(self.wolf)


        self.tile_set = tileset.Tileset("./Assets/tilesheet_forest_house.png",16,16)
        self.tile_map = tilemap.Tilemap("./Assets/tile_map.txt")
        self.solid_codes = [16,17,19,20,23,24,27,28,32,33,35,36,38,39,46,47,50,51,54,55,57,58,61,62]
        self.house_codes = [70,71,72,73,75,76,77,78,80,81,82,83,84,85,86,87,88,89,91,92,93,96]
        self.solid_obj = self.tile_map.find_solid_tiles(self.solid_codes,self.tile_set)
        self.house = self.tile_map.find_solid_tiles(self.house_codes,self.tile_set)
        combined_solid_house_group = self.solid_obj.copy()
        for sprite in self.house:
            combined_solid_house_group.add(sprite)


        flower_sheet = pygame.image.load("./Assets/Flowers_With_Outline_SpriteSheet.png")
        flower_list = []
        for j in range(2):
            for i in range(6):
                flower_image = self.get_image(flower_sheet, i, j, 32, 32, 1, (0,0,0))    
                flower_list.append(flower_image)
        self.flowers_group = object.Object.place_random_objects(30,flower_list,combined_solid_house_group,self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        self.bump_sound = pygame.mixer.Sound("./Assets/freesound_community-small-drum-86171.mp3")
        self.pick_sound = pygame.mixer.Sound("./Assets/freesound_community-pause-piano-sound-40579.mp3")
        self.lost_life_sound = pygame.mixer.Sound("./Assets/universfield-falling-game-character-352287.mp3")
        

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
        x0,y0 = self.player.x,self.player.y
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
        self.player.get_rectangle()
        if pygame.sprite.spritecollide(self.player,self.solid_obj,False, pygame.sprite.collide_mask):
            self.player.x,self.player.y = x0,y0
            self.bump_sound.play()
        self.player.get_rectangle()

        if pygame.sprite.spritecollide(self.player,self.house,False, pygame.sprite.collide_mask):
            return "game_win"
        
        for enemy in self.enemies:
            if isinstance(enemy,character.Wolf):
                x0,y0 = enemy.x,enemy.y
                enemy.move((self.player.x,self.player.y))
                enemy.get_rectangle()
                if pygame.sprite.spritecollide(enemy,self.solid_obj,False, pygame.sprite.collide_mask):
                    enemy.x,enemy.y = x0,y0
                self.check_inside_screen(enemy,self.SCREEN_WIDTH,self.SCREEN_HEIGHT)
            else:
                enemy.move()
                if self.check_inside_screen(enemy,self.SCREEN_WIDTH,self.SCREEN_HEIGHT) == False:
                    enemy.speed = -enemy.speed
            enemy.get_rectangle()
        
        if pygame.sprite.spritecollide(self.player,self.enemies,False,pygame.sprite.collide_mask):
            self.player.numlives -=1
            self.lost_life_sound.play()
            pygame.time.delay(500)
            if self.player.numlives == 0:
                return "game_over"
            else:
                self.player.x,self.player.y = self.START_POS
                self.wolf.x,self.wolf.y = self.WOLF_POS
                self.wolf.get_rectangle()
                self.player.get_rectangle()
        
        for flower in self.flowers_group:
            if pygame.sprite.collide_rect(self.player,flower):
                GameState.Score += 10
                self.pick_sound.play()
                flower.kill()
        return "game"
    

    def draw(self,screen):
        screen.fill(self.BG_COLOUR)
        pygame.draw.rect(screen,(0,0,0),(0,self.SCREEN_HEIGHT,self.SCREEN_WIDTH,self.PANEL_HEIGHT))
        self.tile_map.draw(screen,self.tile_set)
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
                self.click_sound.play()
                pygame.time.delay(500)
                return "main_menu"
            elif self.continue_button.is_pressed(event):
                self.click_sound.play()
                pygame.time.delay(500)
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
                self.click_sound.play()
                pygame.time.delay(500)
                return "main_menu"
            elif self.quit_button.is_pressed(event):
                self.click_sound.play()
                pygame.time.delay(500)
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


class GameWin(GameState):

    def __init__(self,screen_width,screen_height,panel_height):
        super().__init__(screen_width,screen_height,panel_height)
        self.bg_image = pygame.image.load("./Assets/win_bg_800_660.jpg")
        self.menu_button = button.Button("MAIN MENU",self.font2,self.BUTTON_COLOUR,self.HOVERED_COLOUR,(30,50),300,75,20)
        self.quit_button = button.Button("QUIT GAME",self.font2,self.BUTTON_COLOUR,self.HOVERED_COLOUR,(30,570),300,75,20)

    def handle_events(self, events):
        for event in events:
            if self.menu_button.is_pressed(event):
                self.click_sound.play()
                pygame.time.delay(500)
                return "main_menu"
            elif self.quit_button.is_pressed(event):
                self.click_sound.play()
                pygame.time.delay(500)
                return "quit"
        return "game_win"

    def draw(self,screen):
        screen.blit(self.bg_image, (0, 0))
        text_red = self.font2_big.render("YOU WIN!", True, self.RED_TEXT_COLOUR)
        text_black = self.font2_big.render("YOU WIN!", True, (0,0,0))
        screen.blit(text_black,(340,150))
        screen.blit(text_red,(337, 147))
        self.menu_button.draw(screen)
        self.quit_button.draw(screen)
        text_score_red = self.font2.render(f"YOUR SCORE: {GameState.Score}", True, self.RED_TEXT_COLOUR)
        text_score_black = self.font2.render(f"YOUR SCORE: {GameState.Score}", True, (0,0,0))
        screen.blit(text_score_black,(350, 250))
        screen.blit(text_score_red,(347, 247))
