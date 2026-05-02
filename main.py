import pygame

import gamestate



class Game:

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 592
    PANEL_HEIGHT = 68

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Game.SCREEN_WIDTH,Game.SCREEN_HEIGHT + Game.PANEL_HEIGHT))
        pygame.display.set_caption("PyGame Red Hood")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = "main_menu"
        self.score=0

        self.states = {
            "main_menu": gamestate.MainMenu(Game.SCREEN_WIDTH,Game.SCREEN_HEIGHT,Game.PANEL_HEIGHT),
            "game": gamestate.GameScreen(Game.SCREEN_WIDTH,Game.SCREEN_HEIGHT,Game.PANEL_HEIGHT),
            "pause": gamestate.Pause(Game.SCREEN_WIDTH,Game.SCREEN_HEIGHT,Game.PANEL_HEIGHT),
            "game_over": gamestate.GameOver(Game.SCREEN_WIDTH,Game.SCREEN_HEIGHT,Game.PANEL_HEIGHT)
        }

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            next_state = self.states[self.current_state].handle_events(events)
            if self.current_state == "main_menu" and next_state == "game":
                gamestate.GameState.Score = 0
                self.states["game"] = gamestate.GameScreen(Game.SCREEN_WIDTH,Game.SCREEN_HEIGHT,Game.PANEL_HEIGHT)
            if next_state == "quit":
                self.running = False
                continue
            self.current_state = next_state
            self.states[self.current_state].draw(self.screen)
            self.clock.tick(40)
            pygame.display.flip()
        pygame.quit()

game = Game()
game.run()