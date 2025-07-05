import pygame as pg


class Alien():
    def __init__(self, type, pos):
        self.type = type
        self.sprites = [pg.image.load(f"./sprites/alien{type}_{i}") for i in range(1, 2 + 1)]

        self.sprite_index = 0
        self.rect = self.sprites[self.sprite_index].get_rect(topleft=pos)

    def update(self):
        self.move()

    def move(self):
        pass

    def fire(self):
        pass
    
    def draw(self, surface: pg.Surface):
        surface.blit(self.sprites[self.sprite_index], self.rect)


class Aliens():
    def __init__(self):
        pass

    def update(self, dt):
        pass

    def draw(self, surface: pg.Surface):
        pass