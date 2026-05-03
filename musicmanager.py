import pygame


class MusicManager:
    def __init__(self,state="main_menu"):
        self.music = {
            "main_menu": ("./Assets/exploracion_002.wav", -1),
            "game": ("./Assets/Forest_light_and_shadows.ogg", -1),
            "pause": ("./Assets/exploracion_002.wav", -1),
            "game_over": ("./Assets/lightyeartraxx-kl-bells-game-over-iii-416388.mp3", 3),
            "game_win": ("./Assets/aberrantrealities-loud-fanfare-trumpet-effect-01-412045.mp3",3)
        }
        self.curent_state = state
    
    def play(self):
        song, repeat_flag = self.music[self.curent_state]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(repeat_flag)
    
    def stop(self):
        pygame.mixer.music.stop()
    
    def update(self,state):
        if state != self.curent_state:
            self.stop()
            self.curent_state = state
            self.play()