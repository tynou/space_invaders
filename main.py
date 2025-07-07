import sys
import random
import math

from alien import Aliens
from spaceship import Spaceship
from bunker import Bunkers
from ui import Score, LifeCounter, InputBox, TextLabel, TextButton
from leaderboard import Leaderboard
from scene import Menu, Game, NameSelection, LeaderboardMenu
from config import *

import pygame as pg


class SpaceInvaders:
    def __init__(self):
        self.screen_surface = pg.display.set_mode(WORLD_SIZE)
        pg.display.set_caption("space invaders")

        self.scene = Menu(self.handle_event)

        self.update_time_delay = 0

        self.leaderboard = Leaderboard()
    
    def handle_event(self, event):
        match event:
            case "game":
                self.to_game()
            case "name_selection":
                self.to_name_selection()
            case "leaderboard":
                self.to_leaderboard()
            case "menu":
                self.to_menu()
            case _:
                return
    
    def to_game(self):
        self.scene = Game(self.handle_event)

    def to_name_selection(self):
        self.scene = NameSelection(self.handle_event)
    
    def to_leaderboard(self):
        self.scene = LeaderboardMenu(self.handle_event)
    
    def to_menu(self):
        self.scene = Menu(self.handle_event)

    def start(self):
        clock = pg.time.Clock()
        while True:
            dt = clock.tick()

            update_count = self.get_update_count(dt)
            if update_count > 0:
                self.update(update_count * UPDATE_PERIOD)

                self.draw()

    def get_update_count(self, dt):
        self.update_time_delay += dt
        update_count = self.update_time_delay // UPDATE_PERIOD

        self.update_time_delay %= UPDATE_PERIOD

        return update_count
    
    def update(self, dt):
        events = self.get_events()

        self.scene.update(dt, events)

    def draw(self):
        self.screen_surface.fill((0, 0, 0))

        self.scene.draw(self.screen_surface)

        pg.display.flip()

    def get_events(self):
        events = []
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            events.append(event)
        return events


if __name__ == "__main__":
    pg.init()
    game = SpaceInvaders()
    game.start()
