import pygame


class MusicManager:
    """
    En klass som styr musikuppspelning i programmet.

    Attribut:
        music (typing.Dict[str, typing.Tuple[str, int]]): Dictionaryt som har gamestate-koder som nycklar och tupler av filnamn och upprepningsflaggan som värden. 
        current_state (str): Flaggan för den aktuella skärmen i programmet.
    """


    def __init__(self, state: str = "main_menu") -> None:
        """
        Initierar en instans av MusicManager.

        Parametrar:
            state (str): Flaggan för den aktuella skärmen i programmet, standardvärde = "main_menu".
        """

        self.music = {
            "main_menu": ("./Assets/exploracion_002.wav", -1),
            "game": ("./Assets/Forest_light_and_shadows.ogg", -1),
            "pause": ("./Assets/exploracion_002.wav", -1),
            "game_over": ("./Assets/lightyeartraxx-kl-bells-game-over-iii-416388.mp3", 3),
            "game_win": ("./Assets/aberrantrealities-loud-fanfare-trumpet-effect-01-412045.mp3",3)
        }
        self.curent_state = state
    

    def play(self) -> bool:
        """
        En instansmetod som laddar bakgrundsmusik och spelar den.

        Returnerar:
            bool: True om det lyckades att ladda och börja spela musiken.
                False om ett fel uppstod i processen.
        """

        song, repeat_flag = self.music[self.curent_state]
        try:
            pygame.mixer.music.load(song)
            pygame.mixer.music.play(repeat_flag)
            return True
        except pygame.error as err:
            print(f"Can't play the music: {err}")
            return False
    

    def stop(self) -> None:
        """
        En instansmetod som stoppar bakgrundsmusiken.
        """
        
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
    

    def update(self, state: str) -> None:
        """
        En instansmetod som uppdaterar det nuvarande tillståndet av MusicManager-instansen och börjar spela lämplig bakgrundmusik.

        Parametrar:
            state (str): Flaggan för den aktuella skärmen i programmet.
        """
        
        if state != self.curent_state:
            self.stop()
            self.curent_state = state
            self.play()