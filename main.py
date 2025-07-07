import sys
import random
import math

from alien import Aliens
from spaceship import Spaceship
from bunker import Bunkers
from ui import Score, LifeCounter, InputBox, TextLabel, TextButton
from leaderboard import Leaderboard
from config import *

import pygame as pg


class SpaceInvaders:
    def __init__(self):
        self.screen_surface = pg.display.set_mode(WORLD_SIZE)
        pg.display.set_caption("space invaders")

        self.update_time_delay = 0

        self.lives = 3
        self.score = 0

        self.game_over = False

        self.leaderboard = Leaderboard()

        self.scoreboard = Score()
        self.life_counter = LifeCounter()

        self.spaceship = Spaceship()
        self.aliens = Aliens()
        self.bunkers = Bunkers()

        self.input = InputBox(100, 100, 200, 80)

        self.label = TextLabel("score SCORE", 100, 10, 100, 40)

    def start(self):
        clock = pg.time.Clock()
        while True:
            dt = clock.tick()

            update_count = self.get_update_count(dt)
            if update_count > 0:
                if self.game_over:
                    self.reset()

                self.update(update_count * UPDATE_PERIOD)

                self.update_lives()

                self.process_collisions()

                self.draw()
    
    def end_game(self):
        print("DIE")
        self.game_over = True
    
    def reset(self):
        self.spaceship = Spaceship()
        self.aliens.reset()
        self.barricades = Bunkers()
        
        self.lives = 3
        self.score = 0

        self.game_over = False
    
    def update_lives(self):
        if self.spaceship.destroyed:
            if self.lives > 0:
                self.lives -= 1

            if self.lives == 0:
                self.end_game()
            else:
                self.aliens.clear_lasers()
                self.spaceship.reset()

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
        self.life_counter.draw(self.screen_surface, self.lives)

        self.bunkers.draw(self.screen_surface)

        self.spaceship.draw(self.screen_surface)
        self.aliens.draw(self.screen_surface)

        self.input.draw(self.screen_surface)

        self.label.draw(self.screen_surface)

        pg.display.flip()

    def get_events(self):
        events = []
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            events.append(event)
            self.input.handle_event(event)
        return events
    
    def process_collisions(self):
        self.bullet_collisions()
        self.spaceship_and_alien_collisions()
        self.spaceship_and_laser_collisions()
        self.bunker_collisions()
    
    def bullet_collisions(self):
        if not self.spaceship.bullet.active:
            return
        
        for alien in self.aliens:
            if self.spaceship.bullet.rect.colliderect(alien.rect): 
                alien.explode()
                self.spaceship.bullet.set_inactive()

                self.score += alien.type * 10
    
    def spaceship_and_alien_collisions(self):
        if self.spaceship.destroyed:
            return
        
        for alien in self.aliens:
            if alien.rect.colliderect(self.spaceship.rect):
                self.spaceship.destroy()
    
    def spaceship_and_laser_collisions(self):
        if self.spaceship.destroyed:
            return
        
        for laser in self.aliens.lasers:
            if laser.rect.colliderect(self.spaceship.rect):
                self.spaceship.destroy()
                return
    
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
    game = SpaceInvaders()
    game.start()
