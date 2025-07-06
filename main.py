import sys
from typing import List
import random
import math

from alien import Aliens
from spaceship import Spaceship
from bunker import Bunkers
from ui import Score
from config import *

import pygame as pg

SCREENRECT = pg.Rect(0, 0, 500, 500)


class Player(pg.sprite.Sprite):
    speed = 5
    bounce = 50
    gun_offset = 1
    images: List[pg.Surface] = []

    def __init__(self, *groups):
        super().__init__(*groups)
        # self.image = self.images[0]
        self.image = pg.transform.scale_by(self.images[0], 2)
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.reloading = 0
        self.origtop = self.rect.top
        self.facing = -1
    
    def move(self, direction):
        if direction:
            self.facing = direction
        self.rect.move_ip(direction * self.speed, 0)
        self.rect = self.rect.clamp(SCREENRECT)
        self.rect.top = self.origtop - (self.rect.left // self.bounce % 2 * 2)
    
    def gunpos(self):
        pos = self.facing * self.gun_offset + self.rect.centerx
        return pos, self.rect.top

class Alien(pg.sprite.Sprite):
    speed = 13
    animcycle = 12
    images: List[pg.Surface] = []

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.facing = random.choice((-1, 1)) * Alien.speed
        self.frame = 0
        if self.facing < 0:
            self.rect.right = SCREENRECT.right

    def update(self, *args, **kwargs):
        self.rect.move_ip(self.facing, 0)
        if not SCREENRECT.contains(self.rect):
            self.facing = -self.facing
            self.rect.top = self.rect.bottom + 1
            self.rect = self.rect.clamp(SCREENRECT)
        self.frame = self.frame + 1
        self.image = self.images[self.frame // self.animcycle % 3]

class Bullet(pg.sprite.Sprite):
    speed = -11
    images: List[pg.Surface] = []

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        # self.image = self.images[0]
        self.image = pg.transform.scale_by(self.images[0], 1.5)
        self.rect = self.image.get_rect(midbottom=pos)
    
    def update(self, *args, **kwargs):
        self.rect.move_ip(0, self.speed)
        if self.rect.top <= 0:
            self.kill()

class Bomb(pg.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

class Bunker(pg.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)


def load_image(file):
    """loads an image, prepares it for play"""
    file = f"./sprites/{file}"
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
    return surface.convert()


def main():
    screen = pg.display.set_mode((500, 500))
    pg.display.set_caption("space invaders")

    background = pg.Surface(SCREENRECT.size)

    Player.images = [load_image("ship.png")]
    Alien.images = [load_image("alien1_1.png"), load_image("alien1_2.png")]
    Bullet.images = [load_image("boolet.png")]

    bullets = pg.sprite.Group()
    all = pg.sprite.RenderUpdates()

    player = Player(all)

    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        
        keystate = pg.key.get_pressed()

        # clear/erase the last drawn sprites
        all.clear(screen, background)

        # update all the sprites
        all.update()

        direction = keystate[pg.K_RIGHT] - keystate[pg.K_LEFT]
        player.move(direction)

        firing = keystate[pg.K_SPACE]
        if not player.reloading and firing:
            _boolet = Bullet(player.gunpos(), bullets, all)
        player.reloading = firing

        dirty = all.draw(screen)
        pg.display.update(dirty)

        # cap the framerate at 40fps. Also called 40HZ or 40 times per second.
        clock.tick(60)


class SpaceInvaders:
    def __init__(self):
        self.screen_surface = pg.display.set_mode(WORLD_SIZE)
        pg.display.set_caption("space invaders")

        self.update_time_delay = 0

        self.lives = 3
        self.score = 0

        self.scoreboard = Score()

        self.spaceship = Spaceship()
        self.aliens = Aliens()
        self.bunkers = Bunkers()

    def start(self):
        clock = pg.time.Clock()
        while True:
            dt = clock.tick()

            update_count = self.get_update_count(dt)
            if update_count > 0:
                self.update(update_count * UPDATE_PERIOD)

                self.process_collisions()

                self.draw()

    def get_update_count(self, dt):
        self.update_time_delay += dt
        update_count = self.update_time_delay // UPDATE_PERIOD

        self.update_time_delay %= UPDATE_PERIOD

        return update_count
    
    def update(self, dt):
        events = self.get_events()

        self.spaceship.update(dt, events)
        self.aliens.update(dt)

    def draw(self):
        self.screen_surface.fill((0, 0, 0))

        self.scoreboard.draw(self.screen_surface, self.score)

        self.bunkers.draw(self.screen_surface)

        self.spaceship.draw(self.screen_surface)
        self.aliens.draw(self.screen_surface)

        pg.display.flip()

    def get_events(self):
        events = []
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            events.append(event)
        return events
    
    def process_collisions(self):
        self.bullet_collisions()
        self.spaceship_collisions()
        self.bunker_collisions()
    
    def bullet_collisions(self):
        if not self.spaceship.bullet.active:
            return
        
        for alien in self.aliens:
            if self.spaceship.bullet.rect.colliderect(alien.rect): 
                alien.explode()
                self.spaceship.bullet.set_inactive()

                self.score += alien.type * 10
    
    def spaceship_collisions(self):
        for alien in self.aliens:
            if self.spaceship.destroyed:
                return

            if alien.rect.colliderect(self.spaceship.rect):
                self.spaceship.destroy()
    
    def bunker_collisions(self):
        for laser in self.aliens.lasers:
            if self.collide_with_bunkers(laser.rect, BUNKER_EXPLOSION_RADIUS):
                laser.explode()
        
        if not self.spaceship.bullet.active:
            return

        if self.collide_with_bunkers(self.spaceship.bullet.rect, BUNKER_EXPLOSION_RADIUS):
            self.spaceship.bullet.set_inactive()
    
    def collide_with_bunkers(self, rect, radius):
        for bunker in self.bunkers:
            collision_point = self.find_colliding_pixel(rect, bunker)

            if collision_point:
                self.apply_explosion_on_mask(collision_point, radius, bunker)
                self.build_sprite_from_mask(bunker)

                return True

        return False

    def find_colliding_pixel(self, rect, bunker):
        x, y = (rect.x, rect.y)
        offset = (x - bunker.rect.x, y - bunker.rect.y)

        mask = pg.Mask((rect.w, rect.h), fill=True)
        return bunker.mask.overlap(mask, offset)

    def apply_explosion_on_mask(self, collision_point, radius, bunker):
        cx, cy = collision_point
        bunker.mask.set_at((cx, cy), 0)

        for x in range(cx - radius, cx + radius + 1, 1):
            for y in range(cy - radius, cy + radius + 1, 1):

                if x < 0 or x >= bunker.rect.w or y < 0 or y >= bunker.rect.h:
                    continue

                if math.sqrt((x - cx) ** 2 + (y - cy) ** 2) > radius:
                    continue

                if random.random() < BUNKER_DESTRUCTION_PROBABILITY:
                    bunker.mask.set_at((x, y), 0)

    def build_sprite_from_mask(self, bunker):
        surf_array = pg.surfarray.array3d(bunker.sprite)
        for y in range(bunker.rect.h):
            for x in range(bunker.rect.w):
                if bunker.mask.get_at((x, y)) == 0:
                    surf_array[x, y] = (0, 0, 0)

        bunker.sprite = pg.surfarray.make_surface(surf_array)


if __name__ == "__main__":
    pg.init()
    # main()
    game = SpaceInvaders()
    game.start()
