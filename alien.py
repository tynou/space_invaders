from config import *

import pygame as pg


class Alien():
    def __init__(self, type, pos):
        self.type = type
        self.sprites = [pg.image.load(f"./sprites/alien{type}_{i}.png") for i in [1, 2]]

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
        self.rect.x += movement # [0]
        # self.rect.y += movement[1]

    def fire(self):
        pass
    
    def draw(self, surface: pg.Surface):
        if self.exploded:
            return
        
        surface.blit(self.sprites[self.sprite_index], self.rect)
    
    def explode(self):
        self.exploded = True


class Aliens():
    def __init__(self):
        self.aliens = self.init_aliens()
        self.move_amount = 0
        self.movement_speed = ALIEN_SPEED
        self.direction = 1
        self.rect = self.get_rect()
    
    def init_aliens(self):
        aliens = []
        alien_sprites = [[pg.image.load(f"./sprites/alien{type}_{i}.png") for i in [1, 2]] for type in [1, 2, 3]]
        max_w = max([sprites[0].get_rect().w for sprites in alien_sprites])
        max_row_size = max([len(row) for row in ALIEN_FORMATION])
        step = ALIEN_FORMATION_WIDTH_PIXELS / max_row_size
        x0 = (-max_w) // 2 + (WORLD_SIZE[0] - ALIEN_FORMATION_WIDTH_PIXELS) // 2
        xs = [x0 + (step * i) for i in range(max_row_size)]
        for row_index, alien_row in enumerate(ALIEN_FORMATION):
            for i, alien_index in enumerate(alien_row):
                sprites = alien_sprites[alien_index - 1]
                w, h = (sprites[0].get_rect().w, sprites[0].get_rect().h)
                center_x = xs[i]
                center_y = h + (2 * h * row_index) + ALIEN_STARTING_POS_Y
                aliens.append(Alien(alien_index, (center_x - w // 2, center_y - h // 2)))
        return aliens

    def update(self, dt):
        self.remove_dead_aliens()

        movement = self.get_alien_movement(dt)
        for alien in self:
            alien.update(dt, movement)

    def __iter__(self):
        return self.aliens.__iter__()

    def __next__(self):
        return next(self.__iter__())
    
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
    
    def get_alien_movement(self, dt):
        self.move_amount += dt / 1000 * self.movement_speed

        movement = 0 # (0, 0)
        if self.move_amount > 1:
            ps = int(self.move_amount)
            movement = ps * self.direction
            self.move_amount -= ps

        self.rect = self.get_rect()
        self.rect.left += movement # [0]
        # self.rect.top += movement[1]

        if self.direction == 1 and self.rect.right >= WORLD_SIZE[0]:
            movement = movement - (self.rect.right - WORLD_SIZE[0])
            self.direction = -1

        if self.direction == -1 and self.rect.left <= 0:
            movement = movement - self.rect.left
            self.direction = 1

        return movement