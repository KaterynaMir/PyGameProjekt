import pygame

import gamestate

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PANEL_HEIGHT = 60

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT + PANEL_HEIGHT))
pygame.display.set_caption("PyGame Red Hood")

states = {
    "main_menu": gamestate.MainMenu(),
    "game": gamestate.Game(),
    "pause": gamestate.Pause(),
    "game_over": gamestate.GameOver()
}

current_state = "main_menu"

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    next_state = states[current_state].handle_events(events)
    if current_state == "main_menu" and next_state == "game":
        states["game"] = gamestate.Game()
    if next_state == "quit":
        running = False
        continue
    current_state = next_state
    states[current_state].draw(screen)
    clock.tick(40)
    pygame.display.flip()

pygame.quit()