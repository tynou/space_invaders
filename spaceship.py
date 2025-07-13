from config import *

import math

from powerup import Powerup

import pygame as pg


class Spaceship:
    def __init__(self):
        self.sprite = pg.image.load("./sprites/ship.png")
        # self.sprite = pg.transform.scale_by(pg.image.load("./sprites/ship.png"), 2)
        self.rect = self.sprite.get_rect(center=STARTING_POS)

        self.powerups = []

        self.shoot_sound = pg.mixer.Sound("./sounds/shoot.wav")
        self.shoot_sound.set_volume(0.1)
        self.destruction_sound = pg.mixer.Sound("./sounds/explosion.wav")

        self.bullets = []
        self.fire_delay = 0

        self.bullet_direction = (0, -1)

        self.mouse_down = False

        self.move_amount = 0

        self.direction = 0
        self.firing = False

        self.destroyed = False
    
    def reset(self):
        # self.rect = self.sprite.get_rect(center=STARTING_POS)
        self.rect.center = STARTING_POS
        
        self.move_amount = 0

        self.direction = 0
        self.firing = False

        self.destroyed = False
    
    def update(self, dt, events):
        self.handle_events(events)
        self.move(dt)
        self.update_bullets(dt)
        self.fire()

        for powerup in self.powerups:
            powerup.update(dt)

    def handle_events(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                self.firing = True
                self.mouse_down = True
            
            if event.type == pg.MOUSEBUTTONUP:
                self.firing = False
                self.mouse_down = False

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
        
        if self.mouse_down:
            mx, my = pg.mouse.get_pos()
            x, y = self.rect.center
            dx, dy = mx - x, my - y
            magnitude = (dx*dx + dy*dy)**0.5

            self.bullet_direction = (dx / magnitude, dy / magnitude)
        else:
            self.bullet_direction = (0, -1)
    
    def update_bullets(self, dt):
        self.fire_delay += dt

        for bullet in self.bullets:
            if bullet.active:
                bullet.update(dt)

                if bullet.rect.top < 0:
                    bullet.rect.top = 0
                    bullet.explode()
            else:
                self.bullets.remove(bullet)

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

        for bullet in self.bullets:
            bullet.draw(surface)

        for powerup in self.powerups:
            powerup.draw(surface)
    
    def fire(self):
        if not self.firing:
            return
        
        if self.fire_delay < FIRE_INTERVAL:
            return
        
        self.fire_delay = 0
        
        self.bullets.append(Bullet(self.rect.center, self.bullet_direction))
        self.shoot_sound.play()

    def spawn_powerup(self, pos):
        self.powerups.append(Powerup(pos))
    
    def destroy(self):
        self.destroyed = True

        self.destruction_sound.play()


class Bullet:
    def __init__(self, pos, direction):
        self.sprite = pg.image.load("./sprites/bullet.png")
        # self.sprite = pg.transform.rotate(self.sprite, math.degrees(math.atan2(-direction[1], direction[0])))
        self.rect = self.sprite.get_rect(center=pos)

        self.pos = pg.Vector2(pos[0], pos[1])

        self.move_amount = 0

        self.direction = direction
        
        self.active = True
        self.exploded = False
    
    def update(self, dt):
        if not self.active:
            return

        self.move(dt)

    def move(self, dt):
        self.move_amount = dt / 1000 * BULLET_SPEED
        dx, dy = self.direction
        self.pos.x += dx * self.move_amount
        self.pos.y += dy * self.move_amount
        self.rect.center = (self.pos.x, self.pos.y)
        # if self.move_amount > 1:
        #     dx, dy = self.direction
        #     self.rect.x += dx * int(self.move_amount)
        #     self.rect.y += dy * int(self.move_amount)
        #     self.move_amount -= int(self.move_amount)
    
    def draw(self, surface: pg.Surface):
        dx, dy = self.direction
        rotated_sprite = pg.transform.rotate(self.sprite, math.degrees(math.atan2(-dx, -dy)))
        surface.blit(rotated_sprite, self.rect)
    
    def explode(self):
        self.exploded = True
        self.active = False
    
    def set_inactive(self):
        self.active = False
