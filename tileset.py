import pygame

class Tileset:
    def __init__(self, filename, tile_width, tile_height):
        self.image = pygame.image.load(filename).convert_alpha()
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.rect = self.image.get_rect()
        self.tiles=[]

        sheet_width, sheet_height = self.rect.size
        for tile_y in range (0,sheet_height,self.tile_height):
            for tile_x in range (0,sheet_width,self.tile_width):
                tile = pygame.Surface((self.tile_width,self.tile_height))
                tile.blit(self.image, (0,0),(tile_x,tile_y,self.tile_width,self.tile_height))
                tile.set_colorkey((0,0,0))
                self.tiles.append(tile)

