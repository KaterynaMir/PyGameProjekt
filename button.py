import pygame
from typing import Tuple


class Button:
    """ 
    En klass för knappar.
    
    Attribut:
        text (str): Texten som skrivs på knappen.
        base_colour (Tuple[int, int, int]): Färgen (R,G,B) för knappen när musen är utanför knappens område.
        hover_colour (Tuple[int, int, int]): Färgen (R,G,B) för knappen när musen är inom knappens område.
        x (int): Vänster övre x-koordinaten för knappen.
        y (int): Vänster övre y-koordinaten för knappen.
        height (int): Knappens höjd i pixlar.
        width (int): Knappens bredd i pixlar.
        border_radius (int): Parametern som används för att rita knappens rektangel med rundade hörn.
        rect (pygame.Rect): Knappens rektangel som används för att centrera texten på knappen.
        font (pygame.font.Font): Font för texten på knappen.
        is_hovered (bool): Hjälper att växla mellan knappens två färger beroende på musens position.
    """
    BLACK_COLOUR = (0, 0, 0)

    def __init__(self, text: str, font: pygame.font.Font, base_colour: Tuple[int, int, int], hover_colour: Tuple[int, int, int], pos: Tuple[int, int], width: int, height: int, border_radius: int) -> None:
        """ 
        Initierar en Button-instans.

        Parametrar:
            text (str): Texten som skrivs på knappen.
            font (pygame.font.Font): Font för texten på knappen.
            base_colour (Tuple[int, int, int]): Färgen (R,G,B) för knappen när musen är utanför knappens område.
            hover_colour (Tuple[int, int, int]): Färgen (R,G,B) för knappen när musen är inom knappens område.
            pos (Tuple[int, int]): Vänster-topp position för knappen.
            width (int): Knappens bredd i pixlar.
            height (int): Knappens höjd i pixlar.
            border_radius (int): Parametern som används för att rita knappens rektangel med rundade hörn.
        """

        self.text = text
        self.base_colour = base_colour
        self.hover_colour = hover_colour
        self.x,self.y = pos
        self.width = width
        self.height = height
        self.border_radius = border_radius
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.font = font
        self.is_hovered = False

    def draw(self, surface: pygame.Surface) -> None:
        """
        En instansmetod som ritar knappen på ytan(skärmen).

        Parametrar:
            surface (pygame.Surface): Ytan att rita på.
        """

        if self.is_hovered:
            colour = self.hover_colour
        else:
            colour = self.base_colour
        pygame.draw.rect(surface, self.BLACK_COLOUR, (self.x + 3, self.y + 3, self.width, self.height), border_radius = self.border_radius)
        pygame.draw.rect(surface, colour, (self.x, self.y, self.width, self.height), border_radius = self.border_radius)
        rendered_text = self.font.render(self.text, True, self.BLACK_COLOUR)
        rendered_text_rect = rendered_text.get_rect(center = (self.rect.centerx, self.rect.centery))
        surface.blit(rendered_text, rendered_text_rect)

    def is_pressed(self, event: pygame.event.Event) -> bool:
        """
        En instansmetoden som kontrollerar om knappen är tryckt.

        Parametrar:
            event (pygame.event.Event): En händelse från händelsekön.

        Returnerar:
            bool: som visar om knappen är tryckt.
        """

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered == True:
                return True
        return False
