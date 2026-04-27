import pygame


class Button:

    def __init__(self, text, font, base_colour, hover_colour, pos, width, height, border_radius):
        self.text = text
        self.base_colour = base_colour
        self.hover_colour = hover_colour
        self.x,self.y = pos
        self.width = width
        self.height = height
        self.border_radius = border_radius
        self.rect = pygame.Rect(self.x,self.y,width,height)
        self.font = font
        self.is_hovered = False

    def draw(self,surface):
        if self.is_hovered:
            colour = self.hover_colour
        else:
            colour = self.base_colour
        pygame.draw.rect(surface,(0,0,0),(self.x + 3,self.y + 3,self.width,self.height),border_radius=self.border_radius)
        pygame.draw.rect(surface,colour,(self.x,self.y,self.width,self.height),border_radius=self.border_radius)
        rendered_text = self.font.render(self.text, True, (0,0,0))
        rendered_text_rect = rendered_text.get_rect(center = (self.rect.centerx,self.rect.centery))
        surface.blit(rendered_text,rendered_text_rect)

    def is_pressed(self,event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered == True:
                return True
        return False
