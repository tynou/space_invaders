from config import *

import pygame as pg


class Font:
    def __init__(self, scale=1):
        self.availible_letters = "абвгдежзиклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz"
        self.sprites = {letter: pg.transform.scale_by(pg.image.load(f"./sprites/letters/{letter}.png"), scale) for letter in self.availible_letters}
    
    def draw(self, surface: pg.Surface, letter, x, y):
        if letter not in self.sprites:
            return
        
        surface.blit(self.sprites[letter], self.sprites[letter].get_rect(topleft=(x, y)))
    
    def get_letter_width(self, letter):
        if letter not in self.sprites:
            return 0
        
        return self.sprites[letter].get_rect().w

class Score:
    def __init__(self):
        self.digit_sprites = [pg.image.load(f"./sprites/{i}.png") for i in range(0, 10)]
        self.score_sprite = pg.image.load("./sprites/score.png")

    def draw(self, surface: pg.Surface, score):
        score_str = str(score).rjust(5, "0")

        x0, y0 = SCORE_POS
        gap = 8
        rect = self.digit_sprites[0].get_rect()
        rect.topleft = (x0, y0 - (rect.h + 4))
        surface.blit(self.score_sprite, rect)

        for digit in score_str:
            rect.topleft = (x0, y0)
            surface.blit(self.digit_sprites[int(digit)], rect)
            x0 += rect.w + gap

class InputBox:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        # self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.font = Font(2)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ""
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pg.K_SPACE:
                    self.text += " "
                else:
                    letter = event.unicode.lower()
                    if letter not in self.font.availible_letters:
                        return
                    self.text += letter
                # Re-render the text.
                # self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        self.rect.w = max(100, sum(self.font.get_letter_width(letter) for letter in self.text) + 10)

    def draw(self, surface: pg.Surface):
        # self.update()

        # surface.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        x = self.rect.x + 5
        y = self.rect.y + 5
        gap = 4
        space_gap = 12
        for letter in self.text:
            if letter.isspace():
                x += space_gap
                continue
            self.font.draw(surface, letter, x, y)
            x += self.font.get_letter_width(letter) + gap
        
        pg.draw.rect(surface, self.color, self.rect, 2)
        