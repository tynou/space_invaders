from config import *

import pygame as pg


class EventListener:
    def __init__(self):
        self.listeners = {}
    
    def add_event_listener(self, key, func):
        self.listeners[key] = func
    
    def call(self, key):
        if key not in self.listeners:
            return
        
        self.listeners[key]()


class Score:
    def __init__(self):
        self.color = pg.Color(255, 255, 255)
        self.score_text = FONT.render("score:", True, self.color)
        self.score_value = FONT.render("", True, self.color)

    def draw(self, surface: pg.Surface, score):
        self.score_value = FONT.render(str(score).rjust(5, "0"), True, self.color)
        surface.blit(self.score_text, SCORE_POS)
        surface.blit(self.score_value, (SCORE_POS[0], SCORE_POS[1] + 25))


class LifeCounter:
    def __init__(self):
        self.spaceship_sprite = pg.image.load("./sprites/ship.png")
        self.color = pg.Color(255, 255, 255)
        self.text = FONT.render("", True, self.color)

    def draw(self, surface: pg.Surface, lives):
        self.text = FONT.render(str(lives), True, self.color)
        surface.blit(self.text, LIVES_POS)

        for i in range(lives):
            surface.blit(self.spaceship_sprite, (LIVES_POS[0] + 16 + 16 * i, LIVES_POS[1]))

class TextLabel:
    def __init__(self, text, x, y, w, h, color=COLOR_WHITE):
        self.rect = pg.Rect(x, y, w, h)
        self.color = color
        self.text = text
        self.text_surface = FONT.render(text, True, self.color)
    
    def draw(self, surface: pg.Surface):
        surface.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))

class TextButton(EventListener):
    def __init__(self, text, x, y, w, h, color=COLOR_WHITE):
        super().__init__()

        self.rect = pg.Rect(x, y, w, h)
        self.color = color
        self.text = text
        self.text_surface = FONT.render(text, True, self.color)
    
    def update(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.call("down")
    
    def draw(self, surface: pg.Surface):
        border_size = 2 if self.rect.collidepoint(pg.mouse.get_pos()) else 1
        surface.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
        pg.draw.rect(surface, self.color, self.rect, border_size, 2)

class InputBox:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def update(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    if not self.active:
                        self.text = ""
                    self.active = True
                else:
                    self.active = False
                self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            if event.type == pg.KEYDOWN:
                if self.active:
                    if event.key == pg.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif event.key == pg.K_SPACE:
                        self.text += " "
                    else:
                        self.text += event.unicode.lower()
        self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, surface: pg.Surface):
        surface.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        
        pg.draw.rect(surface, self.color, self.rect, 2)
        