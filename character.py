import pygame

class Character(pygame.sprite.Sprite):
    
    def __init__(self,name,image,speed,pos=(0,0)):
        super().__init__()
        self.name = name
        self.image = image
        self.speed = speed
        self.x, self.y = pos
        self.width = image.get_width()
        self.height = image.get_height()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
    
    def draw(self,surface):
        return surface.blit(self.image,(self.x,self.y))
    
    def get_rectangle(self):
        self.rect.topleft = (self.x, self.y)
        return self.rect

class Player(Character):
    
    def __init__(self, name, image, speed, pos, numlives=1):
        super().__init__(name, image, speed, pos)
        self.numlives = numlives
    
    
class Enemy(Character):

    def __init__(self, name, image, speed, pos, direction):
        super().__init__(name, image, speed,pos)
        self.direction = direction
    
    def move(self):
        if self.direction == "H": #horisontal
            self.x += self.speed
        else: # vertical direction
            self.y += self.speed