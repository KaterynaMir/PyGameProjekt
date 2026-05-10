import pygame

import numpy
import object
import tileset
import typing

class Tilemap:
    """
    En klass för tile-kartor som används för att rita på spelens skärm.

    Attribut:
        tile_map_array (numpy.ndarray): 2D int numpy-matris med tile-koder.
        row (int): Antalet rader i tile_map-matrisen.
        col (int): Antalet kolumner i tile_map-matrisen.

        En textfil (filename.txt) med ett nollmatrisutkast för matris(num_row, num_col) kan skapas mha kommandon:
        tile_map = numpy.zeros((num_rows,num_cols),dtype = numpy.uint16)
        numpy.savetxt(filename.txt,tile_map,fmt = "%u")

    """


    def __init__(self, filename: str) -> None:
        """
        Initierar en Tilemap instans.

        Parametrar:
            filename (str): Filnamnet (inklusive sökväg) för .txt-filen som innehåller en 2D int matris med tile-koder.
        """

        self.tile_map_array = numpy.loadtxt(filename, dtype = numpy.uint16 )
        self.row, self.col = self.tile_map_array.shape


    def find_solid_tiles(self, solid_tile_codes: typing.List[int], tile_set: tileset.Tileset) -> pygame.sprite.Group:
        """
        En instansmetod som går igenom tilemap-matrisen och hittar alla hårda tiles på koder från listan,
          sedan skapar objekter från dem och adderar dem till sprite-gruppen.

        Parametrar:
            solid_tile_codes (typing.List[int]): En lista med tile-koder för hårda föremål som Player-karaktären inte kan passera igenom.
            tile_set (tileset.Tileset): En Tileset-objekt som innehåller enstaka tiles bilder.
        
        Returnerar:
            pygame.sprite.Group: en group av hårda sprites som kan kontrolleras för kollision med andra föremål eller karaktärer.
        """

        solid_obj_group=pygame.sprite.Group()
        for i in range(self.row):
            for j in range(self.col):
                tile_code = self.tile_map_array[i, j]
                if tile_code in solid_tile_codes:
                    tile = tile_set.tiles[tile_code]
                    tile_x = j * tile_set.tile_width
                    tile_y = i * tile_set.tile_height
                    solid_obj_group.add(object.Object(tile, (tile_x, tile_y)))
        return solid_obj_group
    
    
    def draw(self, screen: pygame.Surface, tile_set: tileset.Tileset) -> None:
        """
        En instansmetod som ritar tile-kartan på skärmen: går igenom hela tile_map-matrisen och ritar varje tile på skärmen baserat på deras koder.

        Parametrar:
            screen (pygame.Surface): Ytan (skärmen) att rita på.
            tile_set (tileset.Tileset): En Tileset-objekt som innehåller enstaka tile-bilder.
        """

        for i in range(self.row):
            for j in range(self.col):
                tile_code = self.tile_map_array[i, j]
                tile_x = j * tile_set.tile_width
                tile_y = i * tile_set.tile_height
                if tile_code == 0:
                    continue
                tile = tile_set.tiles[tile_code]
                screen.blit(tile,(tile_x,tile_y))

