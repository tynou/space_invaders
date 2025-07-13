from config import *

import math
import random

from powerup import PowerupDrop, TripleShot, Shield
from powerup_types import PowerupTypes

import pygame as pg


class Spaceship:
    def __init__(self, increment_lives):
        self.sprite = pg.image.load(SPRITE_PATH + "ship.png")
        self.rect = self.sprite.get_rect(center=STARTING_POS)

        self.shield_sprite = pg.image.load(SPRITE_PATH + "shield.png")
        self.shield_rect = self.shield_sprite.get_rect(center=STARTING_POS)

        self.increment_lives = increment_lives

        self.powerups = []
        self.current_powerups = []

        self.shoot_sound = pg.mixer.Sound(SOUND_PATH + "shoot.wav")
        self.shoot_sound.set_volume(0.1)
        self.destruction_sound = pg.mixer.Sound(SOUND_PATH + "explosion.wav")

        self.bullets = []
        self.fire_delay = 0

        self.bullet_direction = pg.Vector2(0, -1)

        self.mouse_down = False

        self.move_amount = 0

        self.direction = 0
        self.firing = False

        self.destroyed = False
    
    def reset(self):
        self.rect.center = STARTING_POS
        
        self.move_amount = 0

        self.direction = 0
        self.firing = False

        self.destroyed = False
    
    def update(self, dt, events):
        self.handle_events(events)
        self.move(dt)
        self.update_bullets(dt)
        self.update_powerups(dt)
        self.fire()

    def handle_events(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                self.firing = True
                self.mouse_down = True
            
            if event.type == pg.MOUSEBUTTONUP:
                self.firing = False
                self.mouse_down = False

            if event.type == pg.KEYDOWN:
                if event.key in [pg.K_LEFT, pg.K_a]: self.direction = -1
                if event.key in [pg.K_RIGHT, pg.K_d]: self.direction = 1

                if event.key == pg.K_SPACE: self.firing = True

            if event.type == pg.KEYUP:
                if event.key in [pg.K_LEFT, pg.K_a, pg.K_RIGHT, pg.K_d]: self.direction = 0

                if event.key == pg.K_SPACE: self.firing = False
        
        if self.mouse_down:
            mx, my = pg.mouse.get_pos()
            x, y = self.rect.center
            dx, dy = mx - x, my - y
            magnitude = (dx*dx + dy*dy)**0.5

            self.bullet_direction = pg.Vector2(dx / magnitude, dy / magnitude)
        else:
            self.bullet_direction = pg.Vector2(0, -1)
    
    def update_bullets(self, dt):
        self.fire_delay += dt

        for bullet in self.bullets:
            if bullet.active:
                bullet.update(dt)

                if bullet.rect.top < 0:
                    bullet.explode()
            else:
                self.bullets.remove(bullet)
    
    def update_powerups(self, dt):
        for powerup in self.current_powerups:
            powerup.time_active += dt
            if powerup.time_active > powerup.duration:
                self.current_powerups.remove(powerup)

        for powerup in self.powerups:
            if powerup.active:
                powerup.update(dt)

                if powerup.rect.bottom > WORLD_SIZE[1]:
                    powerup.destroy()
            else:
                self.powerups.remove(powerup)

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
        
        for powerup in self.current_powerups:
            if type(powerup) is Shield:
                self.shield_rect.center = self.rect.center
                surface.blit(self.shield_sprite, self.shield_rect)
    
    def fire(self):
        if not self.firing:
            return
        
        if self.fire_delay < FIRE_INTERVAL:
            return
        
        self.fire_delay = 0

        triple_shot = False
        for powerup in self.current_powerups:
            if type(powerup) is TripleShot:
                triple_shot = True
        
        if triple_shot:
            for angle in [-5, 0, 5]:
                self.bullets.append(Bullet(self.rect.center, self.bullet_direction.rotate(angle)))
        else:
            self.bullets.append(Bullet(self.rect.center, self.bullet_direction))

        self.shoot_sound.play()

    def spawn_powerup(self, pos):
        self.powerups.append(PowerupDrop(random.choice(list(PowerupTypes)), pos))
    
    def apply_powerup(self, powerup):
        match powerup.type:
            case PowerupTypes.HEALTH:
                self.increment_lives()
            case PowerupTypes.TRIPLE_SHOT:
                self.current_powerups.append(TripleShot())
            case PowerupTypes.SHIELD:
                self.current_powerups.append(Shield())
            case _:
                return
    
    def destroy(self):
        self.destroyed = True

        self.destruction_sound.play()


class Bullet:
    def __init__(self, pos, direction):
        self.sprite = pg.image.load("./sprites/bullet.png")
        self.rect = self.sprite.get_rect(center=pos)

        self.position = pg.Vector2(pos[0], pos[1])

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
        dx, dy = self.direction.x, self.direction.y
        self.position.x += dx * self.move_amount
        self.position.y += dy * self.move_amount
        self.rect.center = (self.position.x, self.position.y)
        # if self.move_amount > 1:
        #     dx, dy = self.direction
        #     self.rect.x += dx * int(self.move_amount)
        #     self.rect.y += dy * int(self.move_amount)
        #     self.move_amount -= int(self.move_amount)
    
    def draw(self, surface: pg.Surface):
        dx, dy = self.direction.x, self.direction.y
        rotated_sprite = pg.transform.rotate(self.sprite, math.degrees(math.atan2(-dx, -dy)))
        surface.blit(rotated_sprite, self.rect)
    
    def explode(self):
        self.exploded = True
        self.active = False
    
    def set_inactive(self):
        self.active = False
