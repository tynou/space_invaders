import random
import math

from alien import Aliens
from spaceship import Spaceship
from bunker import Bunkers
from ui import Score, LifeCounter, TextLabel, TextButton, InputBox
from leaderboard import Leaderboard
from config import *

import pygame as pg


class Scene:
    def __init__(self, event_handler):
        self.event_handler = event_handler

    def update(self, dt, events):
        pass

    def draw(self, surface: pg.Surface):
        pass


class Game(Scene):
    def __init__(self, event_handler, username):
        super().__init__(event_handler)

        self.soundtrack = pg.mixer.Sound("./sounds/foregone_destruction.flac")
        self.soundtrack.play(loops=-1)

        self.lives = 3
        self.score = 0

        self.username = username

        self.game_over = False

        self.leaderboard = Leaderboard()

        self.scoreboard = Score()
        self.life_counter = LifeCounter()

        self.spaceship = Spaceship()
        self.aliens = Aliens()
        self.bunkers = Bunkers()
    
    def update(self, dt, events):
        if self.game_over:
            self.reset()

        self.spaceship.update(dt, events)
        self.aliens.update(dt)

        self.update_lives()
        self.process_collisions()

    def draw(self, surface: pg.Surface):
        self.scoreboard.draw(surface, self.score)
        self.life_counter.draw(surface, self.lives)

        self.bunkers.draw(surface)

        self.aliens.draw(surface)
        self.spaceship.draw(surface)
    
    def end_game(self):
        self.game_over = True

        self.leaderboard.add_entry(self.username, self.score)
        self.leaderboard.write_to_file()

        self.soundtrack.stop()

        self.event_handler("menu")
    
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
    
    def process_collisions(self):
        self.bullet_collisions()
        self.spaceship_and_alien_collisions()
        self.spaceship_and_laser_collisions()
        self.bunker_collisions()
    
    def bullet_collisions(self):
        for bullet in self.spaceship.bullets:
            for alien in self.aliens:
                if bullet.rect.colliderect(alien.rect):
                    alien.explode()
                    bullet.explode()
                    self.score += alien.type * 10

                    self.spaceship.spawn_powerup(alien.rect.center)
            
            for laser in self.aliens.lasers:
                if bullet.rect.colliderect(laser.rect):
                    bullet.explode()
                    laser.explode()
        
        # if not self.aliens.mystery_ship.active:
        #     return
        
        # if self.spaceship.bullet.rect.colliderect(self.aliens.mystery_ship.rect):
        #     self.aliens.mystery_ship.explode()
        #     self.spaceship.bullet.set_inactive()

        #     self.score += 300

    
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
        
        for bullet in self.spaceship.bullets:
            if self.collide_with_bunkers(bullet.rect, BUNKER_EXPLOSION_RADIUS):
                bullet.explode()
    
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


class Menu(Scene):
    def __init__(self, event_handler, exit_function):
        super().__init__(event_handler)

        self.title = TextLabel("space invaders", 10, 10, 200, 30)
        self.start_button = TextButton("start", 10, 50, 150, 30)
        self.leaderboard_button = TextButton("leaderboard", 10, 90, 150, 30)
        self.exit_button = TextButton("exit", 10, 130, 150, 30)

        self.start_button.add_event_listener("down", self.to_name_selection)
        self.leaderboard_button.add_event_listener("down", self.to_leaderboard)
        self.exit_button.add_event_listener("down", exit_function)
    
    def to_name_selection(self):
        self.event_handler("name_selection")
    
    def to_leaderboard(self):
        self.event_handler("leaderboard")
    
    def update(self, dt, events):
        self.start_button.update(events)
        self.leaderboard_button.update(events)
        self.exit_button.update(events)

    def draw(self, surface: pg.Surface):
        self.title.draw(surface)
        self.start_button.draw(surface)
        self.leaderboard_button.draw(surface)
        self.exit_button.draw(surface)


class NameSelection(Scene):
    def __init__(self, event_handler):
        super().__init__(event_handler)

        self.name_selection_title = TextLabel("choose your name:", 10, 10, 200, 30)
        self.name = InputBox(10, 50, 200, 30, "name")
        self.play_button = TextButton("play", 10, 90, 150, 30)
        self.back_button = TextButton("back", 10, 130, 150, 30)

        self.play_button.add_event_listener("down", self.to_game)
        self.back_button.add_event_listener("down", self.to_menu)
    
    def to_game(self):
        self.event_handler("game", self.name.text)
    
    def to_menu(self):
        self.event_handler("menu")
    
    def update(self, dt, events):
        self.name.update(events)
        self.play_button.update(events)
        self.back_button.update(events)

    def draw(self, surface: pg.Surface):
        self.name_selection_title.draw(surface)
        self.name.draw(surface)
        self.play_button.draw(surface)
        self.back_button.draw(surface)


class LeaderboardMenu(Scene):
    def __init__(self, event_handler):
        super().__init__(event_handler)

        self.leaderboard = Leaderboard()

        self.leaderboard_title = TextLabel("leaderboard:", 10, 50, 150, 30)
        self.back_button = TextButton("back", 10, 10, 150, 30)

        self.back_button.add_event_listener("down", self.to_menu)

        self.leaders = self.init_list()
    
    def init_list(self):
        leaders = []
        i = 1
        gap = 0
        height = 30
        start_y = 90
        entries = sorted(self.leaderboard.entries.items(), key=lambda entry: -entry[1])
        text_width = max(map(lambda entry: len(entry[0]) * 14, entries))
        for username, score in entries:
            y = start_y + (height + gap) * (i - 1)
            leaders.append([
                TextLabel(str(i), 10, y, 30, height),
                TextLabel(username, 40, y, text_width, height),
                TextLabel(str(score), text_width, y, 60, height)
                ])
            i += 1
        return leaders
    
    def to_menu(self):
        self.event_handler("menu")
    
    def update(self, dt, events):
        self.back_button.update(events)

    def draw(self, surface: pg.Surface):
        self.leaderboard_title.draw(surface)
        self.back_button.draw(surface)

        for counter, username, score in self.leaders:
            counter.draw(surface)
            username.draw(surface)
            score.draw(surface)
            pg.draw.line(surface, pg.Color(255, 255, 255), counter.rect.topright, counter.rect.bottomright, 1)
            pg.draw.line(surface, pg.Color(255, 255, 255), score.rect.topleft, score.rect.bottomleft, 1)
            pg.draw.line(surface, pg.Color(255, 255, 255), counter.rect.bottomleft, score.rect.bottomright, 1)
