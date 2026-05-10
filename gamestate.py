import pygame

import button
import character
import object
import tileset
import tilemap
import typing


class GameState:
    """
    En basklass för spelets tillstånd. Samlar nödvändiga attribut för barnklasser-tillstånder.

        Score (int): Spelets poäng. Klassens attribut.

    Attribut:
        SCREEN_WIDTH (int): Spelets skärmens bredd i pixlar.
        SCREEN_HEIGHT (int): Spelets skärmens höjd i pixlar.
        font1 (pygame.font.Font): Typsnittet för Score och num_lives-attributen som visas i rutan nedanför spel-skärmen.
        font2 (pygame.font.Font): Typsnittet för knappar.
        font2_big (pygame.font.Font): Typsnittet för titlar.
        click_sound (pygame.mixer.Sound): Ljudet för musklick.

    """
    
    #Färgers konstanta
    BLACK_COLOUR = (0, 0, 0)
    WHITE_COLOUR = (255, 255, 255)
    RED_TEXT_COLOUR = (173, 9, 33)  # Färgen för titlar 
    BUTTON_COLOUR = (44, 104, 76)   # Färgen för knappen när musen är utanför knappens område.
    HOVERED_COLOUR = (93, 171, 180) # Färgen för knappen när musen är över knappen (inom knappens område).

    Score = 0 # Spelets poäng

    def __init__(self, screen_width: int, screen_height: int) -> None:
        """
        Initierar en GameState-instans.

        Parametrar:
            screen_width (int): Spelets skärmens bredd i pixlar.
            screen_height (int): Spelets skärmens höjd i pixlar.
        """

        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.font1 = pygame.font.Font("./Assets/Swansea-q3pd.ttf", 32)
        self.font2 = pygame.font.Font("./Assets/Block_Stock.ttf", 28)
        self.font2_big = pygame.font.Font("./Assets/Block_Stock.ttf", 58)
        self.click_sound =  pygame.mixer.Sound("./Assets/universfield-mouse-click-117076.mp3")
        
    def handle_events(self, events: typing.List[pygame.event.Event]) -> None:
        """
        En instansmetod som hanterar händelser i kön.

        Parametrar:
            events (typing.List[pygame.event.Event]): Listan med händelser från händelsekön.
        """
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """
        En instansmetod som ritar spelets tillstånd på skärmen:

        Parametrar:
            screen (pygame.Surface): Ytan att rita på.
        """
        pass
    
    @staticmethod
    def draw_horizontally_centered_text(surface: pygame.Surface, rendered_text: pygame.Surface, y: int) -> pygame.Rect:
        """
        En statisk metod som ritar horisontellt centrerad text på skärmen.

        Parametrar:
            surface (pygame.Surface): Ytan att rita texten på.
            rendered_text (pygame.Surface): En renderad text (textbild) som ska ritas.
            y (int): Y-koordinaten för att placera texten på skärmen
        
        Returnerar:
            pygame.Rect: Rektangeln av den horisontellt centrerade texten på skärmen.
        """
        
        rect= surface.get_rect()
        rendered_text_rect = rendered_text.get_rect(center = (rect.centerx, y))
        surface.blit(rendered_text,rendered_text_rect)
        return rendered_text_rect


class MainMenu(GameState):
    """
    En klass för spelets huvudmeny (MainMenu) tillstånd. Ärver från GameState-klassen.

    Attribut:
        + bg_image (pygame.Surface): En bakgrundsbild för huvudmeny-tillståndet.
        + start_button (button.Button): Startknappen.
        + quit_button (button.Button): Avslutningsknappen.
    """

    def __init__(self, screen_width: int, screen_height: int) -> None:
        """
        Initierar en instans av MainMenu.

        Parametrar:
            screen_width (int): Spelets skärmens bredd i pixlar.
            screen_height (int): Spelets skärmens höjd i pixlar.
        """
        
        super().__init__(screen_width, screen_height)
        self.bg_image = pygame.image.load("./Assets/main_menu_bg_800_660.jpg")
        self.start_button = button.Button("START GAME", self.font2, self.BUTTON_COLOUR, self.HOVERED_COLOUR, (240, 280), 300, 75, 20)
        self.quit_button = button.Button("QUIT GAME", self.font2, self.BUTTON_COLOUR, self.HOVERED_COLOUR, (240, 380), 300, 75, 20)

    def handle_events(self, events: typing.List[pygame.event.Event]) -> str:
        """
        En instansmetod som hanterar händelser i kön.

        Parametrar:
            events (typing.List[pygame.event.Event]): Listan med händelser från händelsekön.
        
        Returnerar:
            str: Nyckeln till nästa speltillstånd.
        """
        for event in events:
            if self.start_button.is_pressed(event): # Startar ett nytt spel.
                self.click_sound.play()
                pygame.time.delay(500)
                return "game"
            elif self.quit_button.is_pressed(event): # Returnerar en flagga för att avsluta programmet.
                self.click_sound.play()
                pygame.time.delay(500)
                return "quit"
        return "main_menu"

    def draw(self, screen: pygame.Surface) -> None:
        """
        En instansmetod som ritar MainMenu-tillståndet på skärmen:

        Parametrar:
            screen (pygame.Surface): Ytan att rita på.
        """
        
        screen.blit(self.bg_image, (0, 0))
        text_red = self.font2_big.render("RED HOOD", True, self.RED_TEXT_COLOUR)
        text_black = self.font2_big.render("RED HOOD", True, self.BLACK_COLOUR)
        screen.blit(text_black,(280, 181))
        screen.blit(text_red,(277, 178))
        self.start_button.draw(screen)
        self.quit_button.draw(screen)
        

class GameScreen(GameState):
    """
    En klass för GameScreen spelets tillstånd. Ärver från GameState-klassen.

    Attribut:
        + PANEL_HEIGHT (int): Höjden på rutan där spelarens poäng och antal liv visas.
        + player (character.Player): Spelarens karaktär.
        + enemies (pygame.sprite.Group): Sprite-gruppen med fiender.
        + wolf (character.Wolf): Varg-fienden.
        + tile_set (tileset.Tileset): Ett Tileset-objekt som innehåller enstaka tile-bilder.
        + tile_map (tilemap.Tilemap): Ett Tilemap-objekt som innehåller tile-kartan. 
        + solid_codes (typing.List[int]): Listan med tile-koder för hårda tiles. 
        + house_codes (typing.List[int]): Listan med tile-koder för målet (mormors hus).
        + solid_obj (pygame.sprite.Group): Sprite-gruppen av hårda objekt för att kontrollera kollisioner med.
        + house (pygame.sprite.Group): Sprite-gruppen med husets tiles.
        + flowers_group (pygame.sprite.Group): Sprite-gruppen med objekt (blommor) som ska samlas för poäng.
        + bump_sound (pygame.mixer.Sound): Stötljudet för spelarens kollisioner med hårda objekt.
        + pick_sound (pygame.mixer.Sound): Ljudet när spelaren samlar blommor och får poäng.
        + lost_life_sound (pygame.mixer.Sound): Ljudet när spelaren förlorar livet och börjar från startpositionen igen.
    """
    
    # Konstanter
    START_POS = (0, 0) # Startpositionen för spelaren.
    WOLF_POS = (750, 450) #  Startpositionen för varg-fienden (Wolf-karaktären).
    BG_COLOUR = (89, 193, 53) #   Bakgrundens färg.

    def __init__(self, screen_width: int, screen_height: int, panel_height: int, pos: typing.Tuple[int, int] = START_POS) -> None:
        """
        Initierar en GameScreen-instans.

        Parametrar:
            screen_width (int): Spelets skärmens bredd i pixlar.
            screen_height (int): Spelets skärmens höjd i pixlar.
            panel_height (int): Höjden på rutan där spelarens poäng och antal liv visas.
            pos (typing.Tuple[int, int]): Startpositionen för spelaren (standardvärde (0, 0)).
        """
       
        super().__init__(screen_width, screen_height)
        self.PANEL_HEIGHT = panel_height

        player_image_sheet = pygame.image.load("./Assets/red-riding-hood_1.png")
        player_image = self.get_image(player_image_sheet, 0, 0, 32, 32, 1.5, self.BLACK_COLOUR)
        self.player = character.Player("Red_hood", player_image, 5, pos, 3)

        enemy1_image_sheet = pygame.image.load("./Assets/Shoom_Idle.png")
        enemy1_image = self.get_image(enemy1_image_sheet, 0, 0, 48, 48, 1, (115, 135, 123))
        enemy1 = character.Enemy("Enemy1", enemy1_image, 4, (0, 400), "H")
        self.enemies = pygame.sprite.Group()
        self.enemies.add(enemy1)

        enemy2_image_sheet = pygame.image.load("./Assets/Dude_Monster_Idle_4.png")
        enemy2_image = self.get_image(enemy2_image_sheet, 0, 0, 32, 32, 1.5, self.BLACK_COLOUR)
        enemy2 = character.Enemy("Enemy2", enemy2_image, 4, (200, 0), "V")
        self.enemies.add(enemy2)

        wolf_image_sheet = pygame.image.load("./Assets/wolf.png")
        wolf_image = self.get_image(wolf_image_sheet, 0, 0, 48, 48, 1, self.WHITE_COLOUR)
        self.wolf = character.Wolf("Wolf", wolf_image, 4, (self.WOLF_POS))
        self.enemies.add(self.wolf)


        self.tile_set = tileset.Tileset("./Assets/tilesheet_forest_house.png", 16, 16)
        self.tile_map = tilemap.Tilemap("./Assets/tile_map.txt")
        self.solid_codes = [16, 17, 19, 20, 23, 24, 27, 28, 32, 33, 35, 36, 38, 39, 46, 47, 50, 51, 54, 55, 57, 58, 61, 62]
        self.house_codes = [70, 71, 72, 73, 75, 76, 77, 78, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 91, 92, 93, 96]
        self.solid_obj = self.tile_map.find_solid_tiles(self.solid_codes, self.tile_set)
        self.house = self.tile_map.find_solid_tiles(self.house_codes, self.tile_set)
        combined_solid_house_group = self.solid_obj.copy()
        for sprite in self.house:
            combined_solid_house_group.add(sprite)


        flower_sheet = pygame.image.load("./Assets/Flowers_With_Outline_SpriteSheet.png")
        flower_list = []
        for j in range(2):
            for i in range(6):
                flower_image = self.get_image(flower_sheet, i, j, 32, 32, 1, self.BLACK_COLOUR)    
                flower_list.append(flower_image)
        self.flowers_group = object.Object.place_random_objects(30, flower_list, combined_solid_house_group, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        self.bump_sound = pygame.mixer.Sound("./Assets/freesound_community-small-drum-86171.mp3")
        self.pick_sound = pygame.mixer.Sound("./Assets/freesound_community-pause-piano-sound-40579.mp3")
        self.lost_life_sound = pygame.mixer.Sound("./Assets/universfield-falling-game-character-352287.mp3")
        

    @staticmethod
    def get_image(sheet: pygame.Surface, frame_x: int, frame_y: int, width: int, height: int, scale: float, colour: typing.Tuple[int, int, int]) -> pygame.Surface:
        """
        En statisk metod som laddar en enstaka bild från bildsarket.

        Parametrar:
            sheet (pygame.Surface): Arket med bilder.
            frame_x (int): Bildrutans index i x-led.
            frame_y (int): Bildrutans index i y-led.
            width (int): Bildrutans bredd i pixlar.
            height (int): Bildrutans höjd i pixlar.
            scale (float): Skalfaktorn.
            colour (typing.Tuple[int, int, int]): Färgen (R, G, B) som ska vara genomskinlig i bilden.

        Returnerar:
            pygame.Surface: Enstaka bilden med genomskinlig bakgrund.
        """
        
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(sheet, (0, 0), (frame_x * width, frame_y * height, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)
        return image


    def handle_events(self, events: typing.List[pygame.event.Event]) -> str:
        """
        En instansmetod som hanterar händelser i kön och innehåller spelets logik.

        Parametrar:
            events (typing.List[pygame.event.Event]): Listan med händelser från händelsekön.
        
        Returnerar:
            str: Nyckeln för nästa tillstånd i spelet.
        """
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: # Om tangentbordsnyckeln "p" trycks pausas spelet.
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

        self.player.check_inside_screen(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.player.get_rectangle()
        if pygame.sprite.spritecollide(self.player, self.solid_obj, False, pygame.sprite.collide_mask):
            self.player.x, self.player.y = x0, y0
            self.bump_sound.play()
        self.player.get_rectangle()

        if pygame.sprite.spritecollide(self.player, self.house, False, pygame.sprite.collide_mask):
            return "game_win" # Om spelaren når mormors hus vinner spelaren och spelet avslutas.
        
        for enemy in self.enemies:
            if isinstance(enemy, character.Wolf):
                x0, y0 = enemy.x, enemy.y
                enemy.move((self.player.x, self.player.y)) # Vargen förföljer spelaren.
                enemy.get_rectangle()
                if pygame.sprite.spritecollide(enemy, self.solid_obj, False, pygame.sprite.collide_mask): # Vargen kan inte gå genom hårda objekt.
                    enemy.x, enemy.y = x0, y0
                enemy.check_inside_screen(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
            else:
                enemy.move()
                if enemy.check_inside_screen(self.SCREEN_WIDTH, self.SCREEN_HEIGHT) == False:
                    enemy.speed = -enemy.speed # Om fienden når skärmens kant byter fienden riktning.
            enemy.get_rectangle()
        
        if pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_mask):
            self.player.num_lives -= 1 # Om spelaren kolliderar med fienden förlorar spelaren ett liv. 
            self.lost_life_sound.play()
            pygame.time.delay(500)
            if self.player.num_lives == 0: # Spelet avslutas om spelaren inte har några liv kvar.
                return "game_over"
            else:
                self.player.x, self.player.y = self.START_POS # Spelaren börjar från startpositionen efter att ha förlörat ett liv.
                self.wolf.x, self.wolf.y = self.WOLF_POS # Vargen börjar också från sin startposition då.
                self.wolf.get_rectangle()
                self.player.get_rectangle()
        
        for flower in self.flowers_group:
            if pygame.sprite.collide_rect(self.player, flower): # Spelaren samlar blommor och får poäng.
                GameState.Score += 10
                self.pick_sound.play()
                flower.kill()

        return "game"
    

    def draw(self, screen: pygame.Surface) -> None:
        """
        En instansmetod som ritar GameScreen-tillståndet på skärmen.

        Parametrar:
            screen (pygame.Surface): Ytan att rita på.
        """
        
        screen.fill(self.BG_COLOUR)
        pygame.draw.rect(screen,self.BLACK_COLOUR,(0,self.SCREEN_HEIGHT,self.SCREEN_WIDTH,self.PANEL_HEIGHT)) # ritar rutan där visas spelarens poäng och antal liv.
        self.tile_map.draw(screen,self.tile_set)
        self.flowers_group.draw(screen)
        self.player.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        text_lives = self.font1.render(f"Lives: {self.player.num_lives}", True, self.WHITE_COLOUR)
        screen.blit(text_lives, (20, self.SCREEN_HEIGHT + 15))
        text_score = self.font1.render(f"Score: {GameState.Score}", True, self.WHITE_COLOUR)
        screen.blit(text_score, (620, self.SCREEN_HEIGHT + 15))


class Pause(GameState):
    """
    En klass för pausens tillstånd i spelet. Ärver från GameState-klassen.

    Attribut:
        + bg_image (pygame.Surface): En bakgrundsbild för pausens tillstånd.
        + menu_button (button.Button): Knappen som växlar till huvudmenyn.
        + continue_button (button.Button): Knappen som växlar till spelskärmen för att återuppta spelet.
    """

    def __init__(self, screen_width: int, screen_height: int) -> None:
        """
        Initierar en instans av pausens tillstånd.

        Parametrar:
            screen_width (int): Spelets skärmens bredd i pixlar.
            screen_height (int): Spelets skärmens höjd i pixlar.
        """
        
        super().__init__(screen_width, screen_height)
        self.bg_image = pygame.image.load("./Assets/paused_bg_800_660.jpg")
        self.menu_button = button.Button("MAIN MENU", self.font2, self.BUTTON_COLOUR, self.HOVERED_COLOUR, (10, 200), 300, 75, 20)
        self.continue_button = button.Button("CONTINUE", self.font2, self.BUTTON_COLOUR, self.HOVERED_COLOUR, (490, 200), 300, 75, 20)


    def handle_events(self, events: typing.List[pygame.event.Event]) -> str:
        """
        En instansmetod som hanterar händelser i kön och växlar mellan spelets tillstånd.

        Parametrar:
            events (typing.List[pygame.event.Event]): Listan med händelser från händelsekön.
        
        Returnerar:
            str: Nyckeln för nästa tillstånd i spelet.
        """

        for event in events:
            if self.menu_button.is_pressed(event): # Växlar till huvudmenyn.
                self.click_sound.play()
                pygame.time.delay(500)
                return "main_menu"
            elif self.continue_button.is_pressed(event): # Växlar till spelets förtsättning.
                self.click_sound.play()
                pygame.time.delay(500)
                return "game"
        return "pause"


    def draw(self, screen: pygame.Surface) -> None:
        """
        En instansmetod som ritar Pause-tillståndet på skärmen.

        Parametrar:
            screen (pygame.Surface): Ytan att rita på.
        """
        
        screen.blit(self.bg_image, (0, 0))
        text_red = self.font2_big.render("GAME PAUSED", True, self.RED_TEXT_COLOUR)
        text_black = self.font2_big.render("GAME PAUSED", True, self.BLACK_COLOUR)
        text_rect = GameState.draw_horizontally_centered_text(screen, text_black, 130)
        screen.blit(text_red, (text_rect.x - 3, text_rect.y - 3))
        self.menu_button.draw(screen)
        self.continue_button.draw(screen)


class GameOver(GameState):
    """
    En klass för GameOver-tillståndet i spelet. Ärver från GameState-klassen.

    Attribut:
        + bg_image (pygame.Surface): En bakgrundsbild för GameOver-tillståndet.
        + menu_button (button.Button): Knappen som växlar till huvudmeny-tillståndet.
        + quit_button (button.Button): Avslutningsknappen.
    """

    def __init__(self, screen_width: int, screen_height: int) -> None:
        """
        Initierar en GameOver-instans.

        Parametrar:
            screen_width (int): Spelets skärmens bredd i pixlar.
            screen_height (int): Spelets skärmens höjd i pixlar.       
        """

        super().__init__(screen_width,screen_height)
        self.bg_image = pygame.image.load("./Assets/game_over_bg_800_660.jpg")
        self.menu_button = button.Button("MAIN MENU", self.font2, self.BUTTON_COLOUR, self.HOVERED_COLOUR, (410, 290), 300, 75, 20)
        self.quit_button = button.Button("QUIT GAME", self.font2, self.BUTTON_COLOUR, self.HOVERED_COLOUR, (410, 410), 300, 75, 20)


    def handle_events(self, events: typing.List[pygame.event.Event]) -> str:
        """
        En instansmetod som hanterar händelser i kön och växlar mellan spelets tillstånd.

        Parametrar:
            events (typing.List[pygame.event.Event]): Listan med händelser från händelsekön.
        
        Returnerar:
            str: Nyckeln till spelets nästa tillstånd.
        """

        for event in events:
            if self.menu_button.is_pressed(event): # Växlar till huvudmenyn.
                self.click_sound.play()
                pygame.time.delay(500)
                return "main_menu"
            elif self.quit_button.is_pressed(event): # Returnerar en flagga för att avsluta programmet.
                self.click_sound.play()
                pygame.time.delay(500)
                return "quit"
        return "game_over"


    def draw(self, screen: pygame.Surface) -> None:
        """
        En instansmetod som ritar GameOver-tillståndet på skärmen.

        Parametrar:
            screen (pygame.Surface): Ytan att rita på.
        """

        screen.blit(self.bg_image, (0, 0))
        text_red = self.font2_big.render("GAME OVER", True, self.RED_TEXT_COLOUR)
        text_black = self.font2_big.render("GAME OVER", True, self.BLACK_COLOUR)
        text_rect = GameState.draw_horizontally_centered_text(screen, text_black, 180)
        screen.blit(text_red, (text_rect.x - 3, text_rect.y - 3))
        self.menu_button.draw(screen)
        self.quit_button.draw(screen)
        text_score_red = self.font2.render(f"YOUR SCORE: {GameState.Score}", True, self.RED_TEXT_COLOUR)
        text_score_black = self.font2.render(f"YOUR SCORE: {GameState.Score}", True, self.BLACK_COLOUR)
        text_score_rect = GameState.draw_horizontally_centered_text(screen, text_score_black, 250)
        screen.blit(text_score_red, (text_score_rect.x - 3, text_score_rect.y - 3))


class GameWin(GameState):
    """
    En klass för GameWin-tillståndet i spelet. Ärver från GameState-klassen.

    Attribut:
        + bg_image (pygame.Surface): En bakgrundsbild för GameWin-tillståndet.
        + menu_button (button.Button): Knappen som växlar till huvudmeny-tillståndet.
        + quit_button (button.Button): Avslutningsknappen.
    """
    def __init__(self, screen_width: int, screen_height: int) -> None:
        """
        Initierar en GameWin-instans.

        Parametrar:
            screen_width (int): Spelets skärmens bredd i pixlar.
            screen_height (int): Spelets skärmens höjd i pixlar.      
        """

        super().__init__(screen_width, screen_height)
        self.bg_image = pygame.image.load("./Assets/win_bg_800_660.jpg")
        self.menu_button = button.Button("MAIN MENU", self.font2, self.BUTTON_COLOUR, self.HOVERED_COLOUR, (30, 50), 300, 75, 20)
        self.quit_button = button.Button("QUIT GAME", self.font2, self.BUTTON_COLOUR, self.HOVERED_COLOUR, (30, 570), 300, 75, 20)


    def handle_events(self, events: typing.List[pygame.event.Event]) -> str:
        """
        En instansmetod som hanterar händelser i kön och växlar mellan spelets tillstånd.

        Parametrar:
            events (typing.List[pygame.event.Event]): Listan med händelser från händelsekön.
        
        Returnerar:
            str: Nyckeln för nästa spelets tillstånd.
        """

        for event in events:
            if self.menu_button.is_pressed(event): # Växlar till huvudmenyn.
                self.click_sound.play()
                pygame.time.delay(500)
                return "main_menu"
            elif self.quit_button.is_pressed(event): # Returnerar en flagga för att avsluta programmet.
                self.click_sound.play()
                pygame.time.delay(500)
                return "quit"
        return "game_win"


    def draw(self, screen: pygame.Surface) -> None:
        """
        En instansmetod som ritar GameWin-tillståndet på skärmen.

        Parametrar:
            screen (pygame.Surface): Ytan att rita på.
        """ 
        screen.blit(self.bg_image, (0, 0))
        text_red = self.font2_big.render("YOU WIN!", True, self.RED_TEXT_COLOUR)
        text_black = self.font2_big.render("YOU WIN!", True, self.BLACK_COLOUR)
        screen.blit(text_black, (340, 150))
        screen.blit(text_red, (337, 147))
        self.menu_button.draw(screen)
        self.quit_button.draw(screen)
        text_score_red = self.font2.render(f"YOUR SCORE: {GameState.Score}", True, self.RED_TEXT_COLOUR)
        text_score_black = self.font2.render(f"YOUR SCORE: {GameState.Score}", True, self.BLACK_COLOUR)
        screen.blit(text_score_black, (350, 250))
        screen.blit(text_score_red, (347, 247))
