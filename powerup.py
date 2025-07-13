from config import *

import pygame as pg


class Powerup:
    def __init__(self, pos):
        self.sprite = pg.image.load("./sprites/health_powerup.png")
        self.rect = self.sprite.get_rect(center=pos)

        self.move_amount = 0

        self.direction = 1
    
    def update(self, dt):
        self.move(dt)

    def move(self, dt):
        self.move_amount += dt / 1000 * POWERUP_SPEED
        if self.move_amount > 1:
            self.rect.y += self.direction * int(self.move_amount)
            self.move_amount -= int(self.move_amount)

    def draw(self, surface: pg.Surface):
        surface.fill(pg.Color(0, 0, 0), pg.Rect(self.rect.left - 5, self.rect.top - 5, self.rect.width + 10, self.rect.height + 10))
        # pg.draw.rect(surface, pg.Color(255, 255, 255), pg.Rect(self.rect.left - 5, self.rect.top - 5, self.rect.width + 10, self.rect.height + 10))
        surface.blit(self.sprite, self.rect)
    
    def destroy(self):
        pass
