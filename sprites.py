import pygame
from const import *
import numpy as np
# from animation import Animator
BASETILEWIDTH = 16
BASETILEHEIGHT = 16


class Spritesheet(object):
    def __init__(self):
        self.sheet = pygame.image.load("spritesheet.png").convert()
        transcolor = self.sheet.get_at((0, 0))
        self.sheet.set_colorkey(transcolor)
        width = int(self.sheet.get_width() / BASETILEWIDTH * TILEWIDTH)
        height = int(self.sheet.get_height() / BASETILEHEIGHT * TILEHEIGHT)
        self.sheet = pygame.transform.scale(self.sheet, (width, height))

    def getImage(self, x, y, width, height):
        x *= TILEWIDTH
        y *= TILEHEIGHT
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())
class PacmanSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.entity = entity
        self.entity.image = self.getStartImage()

    def getStartImage(self):
        return self.getImage(8, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)




class GhostSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.x = 0
        self.entity = entity
        self.entity.image = self.getStartImage()

    def getStartImage(self):
        return self.getImage(self.x, 4)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2 * TILEWIDTH, 2 * TILEHEIGHT)

class MazeSprites(Spritesheet):
        def __init__(self, mazefile):
            Spritesheet.__init__(self)
            self.data = self.readMazeFile(mazefile)

        def getImage(self, x, y):
            return Spritesheet.getImage(self, x, y, TILEWIDTH, TILEHEIGHT)

        def readMazeFile(self, mazefile):
            return np.loadtxt(mazefile, dtype='<U1')

        def constructBackground(self, background, y):
            for row in list(range(self.data.shape[0])):
                for col in list(range(self.data.shape[1])):
                    if self.data[row][col].isdigit():
                        x = int(self.data[row][col]) + 12
                        sprite = self.getImage(x, y)
                        background.blit(sprite, (col * TILEWIDTH, row * TILEHEIGHT))
                    elif self.data[row][col] == '=':
                        sprite = self.getImage(10, 8)
                        background.blit(sprite, (col * TILEWIDTH, row * TILEHEIGHT))

            return background







