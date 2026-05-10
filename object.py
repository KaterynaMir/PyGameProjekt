import pygame

import random
import typing


class Object(pygame.sprite.Sprite):
    """
    En klass för att skapa stationära föremål i spelet, som ärver från pygame.sprite.Sprite. 

    Attribut:
        image (pygame.Surface): Föremålets bild.
        width (int): Föremålets bredd i pixlar.
        height (int): Föremålets höjd i pixlar.
        x (int): Föremålets x-koordinat.
        y (int): Föremålets y-koordinat.
        rect (pygame.Rect): Föremålets rektangel som används för kollisionsdetektering mha colliderect() metoden.
    """
    

    def __init__(self, image: pygame.Surface, pos: typing.Tuple[int, int]) -> None:
        """
        Initierar en Object-instans.

        Parametrar:
            image (pygame.Surface): Föremålets bild.
            pos (typing.Tuple[int, int]: Föremålets position (x, y).
        """
        
        super().__init__()
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.x, self.y = pos
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    
    @staticmethod
    def place_random_objects(num_objects: int, image_list: typing.List[pygame.Surface], solid_obj_group: pygame.sprite.Group, screen_width: int, screen_height: int) -> pygame.sprite.Group:
        """
        En statisk metod som slumpmässigt placerar ett givet antal Object-instanser på spelets skärm så att de inte kolliderar med varandra eller med hårda objekt på skärmen.

        Parametrar:
            num_objects (int): Antalet objekt som ska placeras på skärmen
            image_list (typing.List[pygame.Surface]): Listan med bilder för objekten som ska placeras. Varje nytt objekt får en slumpmassig bild från listan.
            solid_obj_group (pygame.sprite.Group): Sprite-gruppen av hårda objekt för att kontrollera kollisioner med.
            screen_width (int): Spelets skärmens bredd i pixlar.
            screen_height (int): Spelets skärmens höjd i pixlar.
        
        Returnerar:
            pygame.sprite.Group: Sprite-gruppen av slumpmässigt placerade objekt på skärmen.

        """

        obj_group = pygame.sprite.Group()
        for i in range(num_objects):
            obj_image_index = random.randint(0, len(image_list) - 1)
            while True:
                obj_x = random.randint(0, screen_width - image_list[obj_image_index].get_width())
                obj_y = random.randint(0, screen_height - image_list[obj_image_index].get_height())
                obj = Object(image_list[obj_image_index], (obj_x, obj_y))
                if len(pygame.sprite.spritecollide(obj, solid_obj_group, False)) == 0:
                    if i == 0:
                        obj_group.add(obj)
                        break
                    if  len(pygame.sprite.spritecollide(obj, obj_group, False)) == 0:
                        obj_group.add(obj)
                        break
        return obj_group


