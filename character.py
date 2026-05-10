import pygame
import typing

class Character(pygame.sprite.Sprite):
    """
    En klass för spelens karaktärer. Barnklassen till en pygame.sprite.Sprite klass.

    Attribut:
        name (str): Namn på karaktären.
        image (pygame.Surface): Karaktärens bild.
        speed (int): Karaktärens hastighet.
        x (int): Karaktärens x-koordinat.
        y (int): Karaktärens y-koordinat.
        width (int): Karaktärens (bilds) bredd i pixlar.
        height (int): Karaktärens (bilds) höjd i pixlar.
        rect (pygame.Rect objekt): Karaktärens rektangel som används för kollisionsdetektering mha colliderect() metod.
        mask (pygame.mask.Mask objekt): Karaktärens mask som används för kollisionsdetektering mha collidemask() metod.
    """
    

    def __init__(self, name: str, image: pygame.Surface, speed: int, pos: typing.Tuple[int, int] = (0, 0)) -> None:
        """
        Initierar en Charakter-instans.

        Parametrar:
            name (str): Namn på karaktären.
            image (pygame.Surface): Karaktärens bild.
            speed (int): Karaktärens hastighet.
            pos (typing.Tuple[int, int]): (x, y) position för karaktären (standardvärde = (0, 0)).
        """

        super().__init__()
        self.name = name
        self.image = image
        self.speed = speed
        self.x, self.y = pos
        self.width = image.get_width()
        self.height = image.get_height()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
    

    def check_inside_screen(self, screen_width: int, screen_height: int) -> bool:
        """
        En instansmetod som kontrollerar om karaktären är inom skärmen och korrigerar karaktärens koordinater om karaktären är utanför.

        Parametrar:
            screen_width (int): Spelets skärmens bredd i pixlar.
            screen_height (int): Spelets skärmens höjd i pixlar.
        
        Returnerar:
            bool: som är True om karaktätren är inom skärmen och False annars. 
            
        """

        if self.x >= 0 and self.x <= screen_width - self.width:
            if self.y >= 0 and self.y <= screen_height - self.height:
                return True
        self.x = min(max(0, self.x), screen_width - self.width)
        self.y = min(max(0, self.y), screen_height - self.height)
        return False
    

    def draw(self, surface: pygame.Surface) -> None:
        """
        En instansmetod som ritar karaktären på ytan (skärmen).

        Parametrar:
        surface (pygame.Surface): Ytan att rita på.
        """

        surface.blit(self.image, (self.x, self.y))
    

    def get_rectangle(self) -> pygame.Rect:
        """
        En instansmetod som uppdaterar karaktärens rektangels position på karaktärens koordinater.

        Returnerar:
        pygame.Rect: Uppdaterad karaktärens rektangel.
        """

        self.rect.topleft = (self.x, self.y)
        return self.rect


class Player(Character):
    """
    En barnklass till en Character-klass. Skapar spelare-karaktärer.

    Attribut:
        + num_lives (int): Antalet liv för Player-karaktären.
    """
    

    def __init__(self, name: str, image: pygame.Surface, speed: int, pos: typing.Tuple[int, int], num_lives: int) -> None:
        """
        Initierar en Player-instans.

        Parametrar:
            name (str): Namn på Player-karaktären.
            image (pygame.Surface): Player-karaktärens bild.
            speed (int): Player-karaktärens hastighet.
            pos (typing.Tuple[int, int]): (x,y) position för Player-karaktären.
            num_lives (int): Antalet liv för Player-karaktären.
        """

        super().__init__(name, image, speed, pos)
        self.num_lives = num_lives
    
    
class Enemy(Character):
    """
    En barnklass till en Character-klass. Skapar fiender-karaktärer.

    Attribut:
        + direction (str): Anger riktningen för fiendens rörelse ("H" - horisontell, "V" - vertikal).
    """


    def __init__(self, name: str, image: pygame.Surface, speed: int, pos: typing.Tuple[int, int], direction: str = "H") -> None:
        """
        Initierar en Enemy-instans.

        Parametrar:
            name (str): Namn på Enemy-karaktären.
            image (pygame.Surface): Enemy-karaktärens bild.
            speed (int): Enemy-karaktärens hastighet.
            pos (typing.Tuple[int, int]): (x,y) position för Enemy-karaktären.
            direction (str): Riktningen för Enemy-karaktärens rörelse ("H" - horisontell, "V" - vertikal, standardvärde = "H").
        """

        super().__init__(name, image, speed,pos)
        self.direction = direction
    

    def move(self) -> None:
        """
        En instansmetod som flyttar Enemy-karaktären på skärmen.
        """

        if self.direction == "H": #horisontell riktning
            self.x += self.speed
        elif self.direction == "V": # vertikal riktning
            self.y += self.speed


class Wolf(Enemy):
    """
    En barnklass till en Enemy-klass. Sklapar Wolf-fiender som kan förfölja spelare-karaktären.
    """


    def __init__(self, name: str, image: pygame.Surface, speed: int, pos: typing.Tuple[int, int]) -> None:
        """
        Initierar en Wolf-karaktär.

        Parametrar:
            namn (str): Namn på Wolf-karaktären.
            image (pygame.Surface): Wolf-karaktärens bild.
            speed (int): Wolf-karaktärens hastighet.
            pos (typing.Tuple[int, int]): (x,y) position för Wolf-karaktären.
        """
        super().__init__(name, image, speed, pos)
    
    
    def move(self, prey_pos: typing.Tuple[int, int]) -> None:
        """
         En instansmetod som flyttar Wolf-karaktären på skärmen så att avståndet mellan Wolf-karaktären och ens byte minskas.

         Parametrar:
            prey_pos (typing.Tuple[int, int]): position för Wolf-karaktärens byte.
        """
        prey_x, prey_y = prey_pos
        # Först kontrolleras längs vilken koordinat avståndet till bytet är störst, och sedan minskas detta avstånd.
        if abs(self.x - prey_x) >= abs(self.y - prey_y):
            if self.x > prey_x:
                self.x -= self.speed
            elif self.x < prey_x:
                self.x += self.speed
        else:
            if self.y > prey_y:
                self.y -= self.speed
            elif self.y < prey_y:
                self.y += self.speed

