import random

from config import *

import pygame as pg


class Laser:
    def __init__(self, pos):
        self.sprites = [pg.image.load(f"./sprites/laser{i}.png") for i in [1, 2]]
        self.sprite_index = 0
        self.rect = self.sprites[self.sprite_index].get_rect(center=pos)
        self.exploded = False
        self.direction = 1
        self.move_amount = 0

    def update(self, dt):
        self.move(dt)
    
    def move(self, dt):
        if self.exploded:
            return
        self.move_amount += dt / 1000 * LASER_SPEED
        if self.move_amount > 1:
            self.rect.y += self.direction * int(self.move_amount)
            self.move_amount -= int(self.move_amount)

    def draw(self, surface: pg.Surface):
        surface.blit(self.sprites[self.sprite_index], self.rect)
        self.sprite_index = (self.sprite_index + 1) % len(self.sprites)

    def explode(self):
        self.exploded = True


class MysteryShip:
    def __init__(self):
        self.sprite = pg.image.load("./sprites/mystery_ship.png")

        self.rect = self.sprite.get_rect()
        self.direction = 0
        self.move_amount = 0

        self.active = False
        self.exploded = False

    def launch(self, pos, direction):
        self.rect = self.sprite.get_rect(topleft=pos)
        self.direction = direction
        self.active = True

        self.exploded = False

    def update(self, dt):
        self.move(dt)

    def move(self, dt):
        if self.exploded or not self.active:
            return
        self.move_amount += dt / 1000 * MYSTERY_SHIP_SPEED
        if self.move_amount > 1:
            self.rect.x += int(self.move_amount) * self.direction
            self.move_amount -= int(self.move_amount)

    def draw(self, surface: pg.Surface):
        if not self.active:
            return

        surface.blit(self.sprite, self.rect)

    def explode(self):
        self.exploded = True

    def set_inactive(self):
        self.active = False


class Alien:
    def __init__(self, type, pos):
        self.type = type
        self.sprites = [pg.image.load(f"./sprites/alien{type}_{i}.png") for i in [1, 2]]

        self.destroy_sound = pg.mixer.Sound("./sounds/alien_destroyed.wav")

        self.move_amount = 0
        self.last_sprite_shift_delay = 0

        self.sprite_index = 0
        self.rect = self.sprites[self.sprite_index].get_rect(topleft=pos)

        self.exploded = False

    def update(self, dt, movement):
        if self.exploded:
            return
        
        self.move(movement)
        self.sprite_shift(dt)
    
    def sprite_shift(self, dt):
        self.last_sprite_shift_delay += dt
        if self.last_sprite_shift_delay > SPRITE_SHIFT_PERIOD:
            self.sprite_index += 1
            self.sprite_index %= len(self.sprites)
            self.last_sprite_shift_delay -= SPRITE_SHIFT_PERIOD

    def move(self, movement):
        self.rect.x += movement[0]
        self.rect.y += movement[1]

    def fire(self):
        return Laser(self.rect.center)
    
    def draw(self, surface: pg.Surface):
        if self.exploded:
            return
        
        surface.blit(self.sprites[self.sprite_index], self.rect)
    
    def explode(self):
        self.exploded = True
        self.destroy_sound.play()


class Aliens:
    def __init__(self):
        self.aliens = self.init_aliens()
        self.move_amount = 0
        self.movement_speed = ALIEN_SPEED
        self.direction = 1
        self.rect = self.get_rect()
        self.lasers = []
        self.last_firing_time = 0
        self.mystery_ship = MysteryShip()
        self.last_mystery_ship_time = 0

    def reset(self):
        self.aliens = self.init_aliens()
        self.move_amount = 0
        self.movement_speed = ALIEN_SPEED
        self.direction = 1
        self.rect = self.get_rect()
        self.lasers = []
        self.last_firing_time = 0
        self.last_mystery_ship_time = 0
    
    def init_aliens(self):
        aliens = []
        alien_sprites = [[pg.image.load(f"./sprites/alien{type}_{i}.png") for i in [1, 2]] for type in [1, 2, 3]]
        max_w = max([sprites[0].get_rect().w for sprites in alien_sprites])
        max_row_size = max([len(row) for row in ALIEN_FORMATION])
        step = ALIEN_FORMATION_WIDTH / max_row_size
        x0 = (-max_w) // 2 + (WORLD_SIZE[0] - ALIEN_FORMATION_WIDTH) // 2
        xs = [x0 + (step * i) for i in range(max_row_size)]
        for row_index, alien_row in enumerate(ALIEN_FORMATION):
            for i, alien_index in enumerate(alien_row):
                sprites = alien_sprites[alien_index - 1]
                w, h = (sprites[0].get_rect().w, sprites[0].get_rect().h)
                center_x = xs[i]
                center_y = h + (2 * h * row_index) + ALIEN_STARTING_Y
                aliens.append(Alien(alien_index, (center_x - w // 2, center_y - h // 2)))
        return aliens

    def update(self, dt):
        self.fire(dt)

        self.update_lasers(dt)
        self.update_mystery_ship(dt)

        self.remove_dead_aliens()

        if not self.aliens:
            self.reset()
            return

        movement = self.get_alien_movement(dt)
        for alien in self:
            alien.update(dt, movement)

    def __iter__(self):
        return self.aliens.__iter__()

    def __next__(self):
        return next(self.__iter__())
    
    def clear_lasers(self):
        self.lasers = []
    
    def update_lasers(self, dt):
        for laser in self.lasers:

            laser.update(dt)

            if laser.rect.bottom >= WORLD_SIZE[1]:
                laser.explode()

            if laser.exploded:
                self.lasers.remove(laser)
    
    def update_mystery_ship(self, dt):
        self.last_mystery_ship_time += dt
        if self.last_mystery_ship_time > MYSTERY_SHIP_PERIOD:
            self.last_mystery_ship_time -= MYSTERY_SHIP_PERIOD
            self.launch_mystery_ship()

        if not self.mystery_ship.active:
            return

        self.mystery_ship.update(dt)

        if self.mystery_ship.rect.x > WORLD_SIZE[0] or self.mystery_ship.rect.right < 0:
            self.mystery_ship.set_inactive()

        if self.mystery_ship.exploded:
            self.mystery_ship.set_inactive()
    
    def launch_mystery_ship(self):
        index = random.choice([0, 1])
        x = [0, WORLD_SIZE[0] - self.mystery_ship.rect.w][index]
        y = MYSTERY_SHIP_STARTING_Y
        direction = [1, -1][index]

        self.mystery_ship.launch((x, y), direction)

    def fire(self, dt):
        self.last_firing_time += dt

        while self.last_firing_time > LASER_FIRING_PERIOD:
            self.last_firing_time -= LASER_FIRING_PERIOD

            firing_aliens = self.get_firing_aliens()
            if not firing_aliens:
                return
            
            alien = random.choice(firing_aliens)
            self.lasers.append(alien.fire())
    
    def get_firing_aliens(self):
        xs = set(alien.rect.centerx for alien in self.aliens)
        alien_dict = {x: [] for x in xs}
        for alien in self.aliens:
            alien_dict[alien.rect.centerx].append(alien)

        lowest_aliens = []
        for x in xs:
            max_alien = None
            max_alien_y = 0
            for alien in alien_dict[x]:
                if alien.rect.bottom > max_alien_y:
                    max_alien = alien
                    max_alien_y = alien.rect.bottom
            if max_alien: lowest_aliens.append(max_alien)

        return lowest_aliens
    
    def remove_dead_aliens(self):
        for alien in self:
            if alien.exploded:
                self.aliens.remove(alien)
    
    def get_rect(self):

        if not self.aliens:
            return pg.Rect((0, 0), (0, 0))

        x0 = min(alien.rect.left for alien in self.aliens)
        y0 = min(alien.rect.top for alien in self.aliens)
        x1 = max(alien.rect.right for alien in self.aliens)
        y1 = max(alien.rect.bottom for alien in self.aliens)
        rect = pg.Rect(x0, y0, x1 - x0, y1 - y0)
        return rect

    def draw(self, surface: pg.Surface):
        for alien in self:
            alien.draw(surface)
        for laser in self.lasers:
            laser.draw(surface)
        self.mystery_ship.draw(surface)
    
    def get_alien_movement(self, dt):
        self.move_amount += dt / 1000 * self.movement_speed

        movement = (0, 0)
        if self.move_amount > 1:
            ps = int(self.move_amount)
            movement = (ps * self.direction, 0)
            self.move_amount -= ps

        self.rect = self.get_rect()
        self.rect.left += movement[0]
        self.rect.top += movement[1]

        if self.direction == 1 and self.rect.right >= WORLD_SIZE[0]:
            movement = (movement[0] - (self.rect.right - WORLD_SIZE[0]), self.aliens[0].rect.h)
            self.direction = -1

        if self.direction == -1 and self.rect.left <= 0:
            movement = (movement[0] - self.rect.left, self.aliens[0].rect.h)
            self.direction = 1

        return movement