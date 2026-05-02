import pygame

import numpy
import object

class Tilemap:
    def __init__(self,filename):
        self.tile_map=numpy.loadtxt(filename,dtype = numpy.uint16 )
        self.row,self.col = self.tile_map.shape
    
    def find_solid_tiles(self,solid_tile_codes,tile_set):
        solid_obj_group=pygame.sprite.Group()
        for i in range(self.row):
            for j in range(self.col):
                tile_code = self.tile_map[i,j]
                if tile_code in solid_tile_codes:
                    tile = tile_set.tiles[tile_code]
                    tile_x = j*tile_set.tile_width
                    tile_y = i*tile_set.tile_height
                    solid_obj_group.add(object.Object(tile,(tile_x,tile_y)))
        return solid_obj_group
    
    def draw(self,screen,tile_set):
        for i in range(self.row):
            for j in range(self.col):
                tile_code = self.tile_map[i,j]
                tile_x = j*tile_set.tile_width
                tile_y = i*tile_set.tile_height
                if tile_code == 0:
                    continue
                tile = tile_set.tiles[tile_code]
                screen.blit(tile,(tile_x,tile_y))

#tile_map = numpy.zeros((37,50),dtype = numpy.uint16)
#numpy.savetxt("tile_map.txt",tile_map,fmt = "%u")