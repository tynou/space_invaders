import sys

from scene import Menu, Game, NameSelection, LeaderboardMenu
from config import *

import pygame as pg


class SpaceInvaders:
    def __init__(self):
        self.screen_surface = pg.display.set_mode(WORLD_SIZE)
        pg.display.set_caption("space invaders")
        pg.display.set_icon(pg.image.load("./sprites/icon.png"))

        self.scene = Menu(self.handle_event, self.exit)

        self.update_time_delay = 0
    
    def handle_event(self, event, *args):
        match event:
            case "game":
                self.to_game(*args)
            case "name_selection":
                self.to_name_selection(*args)
            case "leaderboard":
                self.to_leaderboard(*args)
            case "menu":
                self.to_menu(*args)
            case _:
                return
    
    def to_game(self, username):
        self.scene = Game(self.handle_event, username)

    def to_name_selection(self):
        self.scene = NameSelection(self.handle_event)
    
    def to_leaderboard(self):
        self.scene = LeaderboardMenu(self.handle_event)
    
    def to_menu(self):
        self.scene = Menu(self.handle_event, self.exit)

    def start(self):
        clock = pg.time.Clock()
        while True:
            dt = clock.tick()

            update_count = self.get_update_count(dt)
            if update_count > 0:
                self.update(update_count * UPDATE_PERIOD)

                self.draw()
    
    def exit(self):
        sys.exit()

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
                self.exit()
            events.append(event)
        return events


if __name__ == "__main__":
    pg.init()
    game = SpaceInvaders()
    game.start()
