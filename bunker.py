from config import *

import pygame as pg


class Bunker:
    def __init__(self, pos):
        self.sprite = pg.image.load("./sprites/bunker.png")
        self.rect = self.sprite.get_rect(center=pos)
        self.mask = pg.mask.from_threshold(self.sprite, (0, 0, 0, 0), (1, 1, 1, 255))
        self.mask.invert()
    
    def draw(self, surface: pg.Surface):
        surface.blit(self.sprite, self.rect)

class Bunkers:
    def __init__(self):
        self.bunkers = [Bunker(pos) for pos in BUNKER_POSITIONS]

    def draw(self, surface: pg.Surface):
        for bunker in self.bunkers:
            bunker.draw(surface)

    def __iter__(self):
        return self.bunkers.__iter__()

    def __next__(self):
        return next(self.__iter__())
