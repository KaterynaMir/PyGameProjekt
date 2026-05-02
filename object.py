import pygame

import random


class Object(pygame.sprite.Sprite):
    
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.x, self.y = pos
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
    
    
    @staticmethod
    def place_random_objects(num_objects,image_list,solid_obj_group,screen_width, screen_height):
        obj_group = pygame.sprite.Group()
        for i in range(num_objects):
            obj_image_index = random.randint(0,len(image_list)-1)
            while True:
                obj_x = random.randint(0,screen_width-image_list[obj_image_index].get_width())
                obj_y = random.randint(0,screen_height-image_list[obj_image_index].get_height())
                obj = Object(image_list[obj_image_index],(obj_x,obj_y))
                if len(pygame.sprite.spritecollide(obj,solid_obj_group,False)) == 0:
                    if i==0:
                        obj_group.add(obj)
                        break
                    if  len(pygame.sprite.spritecollide(obj,obj_group,False)) == 0:
                        obj_group.add(obj)
                        break
        return obj_group


