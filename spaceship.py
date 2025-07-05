from config import *

import pygame as pg


class Spaceship():
    def __init__(self):
        self.sprite = pg.image.load("./sprites/ship.png")
        # self.sprite = pg.transform.scale_by(pg.image.load("./sprites/ship.png"), 2)
        self.rect = self.sprite.get_rect(center=STARTING_POS)

        self.bullet = Bullet()

        self.move_amount = 0

        self.direction = 0
        self.firing = False
    
    def update(self, dt, events):
        self.handle_events(events)
        self.move(dt)
        self.update_bullet(dt)
        self.fire()

    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.direction = -1

                if event.key == pg.K_RIGHT:
                    self.direction = 1

                if event.key == pg.K_SPACE:
                    self.firing = True

            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    self.direction = 0

                if event.key == pg.K_RIGHT:
                    self.direction = 0

                if event.key == pg.K_SPACE:
                    self.firing = False
    
    def update_bullet(self, dt):
        if not self.bullet.active:
            return

        self.bullet.update(dt)

        if self.bullet.rect.top < 0:
            self.bullet.rect.top = 0
            self.bullet.explode()

        if self.bullet.time_since_explosion > EXPLOSION_DURATION:
            self.bullet.set_inactive()

    def move(self, dt):
        self.move_amount += dt / 1000 * SPACESHIP_SPEED
        if self.move_amount > 1:
            self.rect.x += int(self.move_amount) * self.direction
            self.move_amount -= int(self.move_amount)
            if self.rect.left < 0:
                self.rect.x = 0
            if self.rect.right >= WORLD_SIZE[0]:
                self.rect.right = WORLD_SIZE[0] - 1

    def draw(self, surface: pg.Surface):
        surface.blit(self.sprite, self.rect)

        if self.bullet.active:
            self.bullet.draw(surface)
    
    def fire(self):
        if not self.firing:
            return
        
        if self.bullet.active:
            return
        
        self.bullet.launch(self.rect.center)


class Bullet():
    def __init__(self):
        self.sprite = pg.image.load("./sprites/boolet.png")
        # self.sprite = pg.transform.scale_by(pg.image.load("./sprites/boolet.png"), 2)
        self.rect = None

        self.move_amount = 0
        self.time_since_explosion = 0
        
        self.active = False
        self.exploded = False
    
    def launch(self, pos):
        self.active = True
        self.exploded = False
        self.time_since_explosion = 0
        self.move_amount = 0
        self.rect = self.sprite.get_rect(center=pos)
    
    def update(self, dt):
        if not self.active:
            return

        if self.exploded:
            self.time_since_explosion += dt
        else:
            self.move(dt)

    def move(self, dt):
        self.move_amount += dt / 1000 * BULLET_SPEED
        if self.move_amount > 1:
            self.rect.y += -int(self.move_amount)
            self.move_amount -= int(self.move_amount)
    
    def draw(self, surface: pg.Surface):
        surface.blit(self.sprite, self.rect)
    
    def explode(self):
        self.exploded = True
    
    def set_inactive(self):
        self.active = False
