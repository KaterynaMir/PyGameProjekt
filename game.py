import pygame
import musicmanager
import gamestate

class Game:
    """
    En klass som styr spelet.

    Attribut:
        screen (pygame.Surface): Spelets fönster (skärm).
        clock (pygame.time.Clock): Klockan.
        running (bool): Flaggan för att köra spelet. 
        current_state (str): Nyckeln för spelets tillstånd.
        music_manager (musicmanager.MusicManager): En instans av musikhanteraren.
        states (typing.Dict[str, gamestate.GameState]): Diktionaryt som har speltillståndskoder som nycklar och speltillståndsobjekt som värden. 
    """

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 592
    PANEL_HEIGHT = 68

    def __init__(self) -> None:
        """
        Initierar en Game-instans.
        """

        pygame.init()
        self.screen = pygame.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT + Game.PANEL_HEIGHT))
        pygame.display.set_caption("PyGame Red Hood")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = "main_menu"
        self.music_manager = musicmanager.MusicManager()

        self.states = {
            "main_menu": gamestate.MainMenu(Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT + Game.PANEL_HEIGHT),
            "game": gamestate.GameScreen(Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT, Game.PANEL_HEIGHT),
            "pause": gamestate.Pause(Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT + Game.PANEL_HEIGHT),
            "game_over": gamestate.GameOver(Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT + Game.PANEL_HEIGHT),
            "game_win": gamestate.GameWin(Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT + Game.PANEL_HEIGHT)
        }


    def run(self) -> None:
        """
        En instansmetod som kör spelet.
        """

        self.music_manager.play()
        
        while self.running:

            events = pygame.event.get() # Får alla händelser från kön.
            for event in events:
                if event.type == pygame.QUIT: 
                    self.running = False # Avslutar spelet
    
            next_state = self.states[self.current_state].handle_events(events) # Hanterar händelser för nuvarande speltillstånd.

            if self.current_state == "main_menu" and next_state == "game":
                gamestate.GameState.Score = 0 # Sätter poängen till noll för ett nytt spel.
                self.states["game"] = gamestate.GameScreen(Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT, Game.PANEL_HEIGHT)

            if next_state == "quit": # Flaggan för att avsluta spelet.
                self.running = False # Avslutar spelet.
                continue

            self.music_manager.update(next_state) # Uppdaterar bakgrundsmusik.
            self.current_state = next_state # Uppdaterar spelltillståndets nyckel.
            self.states[self.current_state].draw(self.screen) # Ritar uppdaterat speltillstånd på skärmen.
            self.clock.tick(40) # Skärmens uppdateringsfrekvens.
            pygame.display.flip() # Uppdaterar skärmen.

        self.music_manager.stop()
        pygame.quit()
