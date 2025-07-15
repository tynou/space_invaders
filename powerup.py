from config import *

from powerup_types import PowerupTypes

import pygame as pg


class PowerupDrop:
    def __init__(self, type, pos):
        self.sprite = pg.image.load(SPRITE_PATH + POWERUP_SPRITES[type])
        self.rect = self.sprite.get_rect(center=pos)

        self.type = type

        self.move_amount = 0

        self.direction = 1

        self.active = True
    
    def update(self, dt):
        self.move(dt)

    def move(self, dt):
        self.move_amount += dt / 1000 * POWERUP_SPEED
        if self.move_amount > 1:
            self.rect.y += self.direction * int(self.move_amount)
            self.move_amount -= int(self.move_amount)

    def draw(self, surface: pg.Surface):
        surface.fill(pg.Color(0, 0, 0), pg.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height))
        surface.blit(self.sprite, self.rect)
    
    def destroy(self):
        self.active = False


class TripleShot:
    def __init__(self):
        self.type = PowerupTypes.TRIPLE_SHOT
        self.time_active = 0
        self.duration = 5000

class Shield:
    def __init__(self):
        self.type = PowerupTypes.SHIELD
        self.time_active = 0
        self.duration = 5000
