import pygame
from settings import *
import pytmx

class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha = True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x,y,gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile,(x*self.tmxdata.tilewidth,y*self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pygame.Surface((self.width,self.height),pygame.HWSURFACE|pygame.SRCALPHA)
        self.render(temp_surface)
        return temp_surface

## OLD MAP
#class Map:
#    def __init__(self, filename):
#        self.data = []
#        with open(filename, 'rt') as f:
#            for line in f:
#                self.data.append(line.strip())
#
#        self.tilewidth = len(self.data[0])
#        self.tileheight = len(self.data)
#        self.width = self.tilewidth * TILE_SIZE
#        self.height = self.tileheight * TILE_SIZE

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0,0,width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self,target):
        x = -target.rect.centerx + int(MAP_WIDTH/2)
        y = -target.rect.centery + int(MAP_HEIGHT/2)
        # limit scrollin map
        x = min(0,x)
        y = min(0,y)
        x = max(-(self.width - MAP_WIDTH), x)
        y = max(-(self.height - MAP_HEIGHT), y)

        self.camera = pygame.Rect(x,y,self.width, self.height)


