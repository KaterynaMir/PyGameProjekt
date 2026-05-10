import pygame

class Tileset:
    """
    En klass för tiles uppsättning. Laddar individuella tiles från tile-arket som bilder (pygame.Surface) och lagrar dem i en lista. 

    Attribut:
        image (pygame.Surface): En tile-arkets bild (innehåller alla tiles).
        tile_width (int): Bredden i pixlar för en tile.
        tile_height (int): Höjden i pixlar för en tile.
        rect (pygamr.Rect): Rektangeln för hela tile-arkets bild.
        tiles (List[pygame.Surface]): Listan med individuella tile-bilder.
    """


    def __init__(self, filename: str, tile_width: int, tile_height: int) -> None:
        """
        Initierar en Tileset-instans.

        Parametrar:
            filename (str): Filnamnet (inklusive sökväg) för tile-arkets fil.
            tile_width (int): Bredden i pixlar för en tile.
            tile_height (int): Höjden i pixlar för en tile.
        """

        self.image = pygame.image.load(filename).convert_alpha()
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.rect = self.image.get_rect()
        self.tiles=[]

        sheet_width, sheet_height = self.rect.size
        for tile_y in range (0, sheet_height, self.tile_height):
            for tile_x in range (0, sheet_width, self.tile_width):
                tile = pygame.Surface((self.tile_width, self.tile_height))
                tile.blit(self.image, (0, 0),(tile_x, tile_y, self.tile_width, self.tile_height))
                tile.set_colorkey((0, 0, 0))
                self.tiles.append(tile)

