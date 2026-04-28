import pygame

class Character:
    
    def __init__(self,name,image,speed,numlives=1):
        self.name = name
        self.image = image
        self.speed = speed
        self.width = image.get_width()
        self.height = image.get_height()
        self.x = 0
        self.y = 0
        self.numlives = numlives
    
    def draw(self,surface):
        return surface.blit(self.image,(self.x,self.y))
    
    def get_rectangle(self):
        return pygame.Rect(self.x,self.y,self.width,self.height)

class Player(Character):
    
    def __init__(self,name,image,speed,numlives=1):
        super().__init__(name,image,speed,numlives)
    
    
class Enemy(Character):

    def __init__(self, name, image, speed, pos, direction):
        super().__init__(name, image, speed)
        self.x,self.y = pos
        self.direction = direction
    
    def move(self):
        if self.direction == "H": #horisontal
            self.x += self.speed
        else: # vertical direction
            self.y += self.speed