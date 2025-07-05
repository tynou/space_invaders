from config import *

import pygame as pg

class Score:
    def __init__(self):
        self.digit_sprites = [pg.image.load(f"./sprites/{i}.png") for i in range(0, 10)]
        self.score_sprite = pg.image.load("./sprites/score.png")

    def draw(self, surface: pg.Surface, score):
        score_str = str(score).rjust(5, "0")

        x0, y0 = SCORE_POS
        step = 8
        r = self.digit_sprites[0].get_rect()
        r.topleft = (x0, y0 - (r.h * 2))
        surface.blit(self.score_sprite, r)

        for digit in score_str:
            r.topleft = (x0, y0)
            surface.blit(self.digit_sprites[int(digit)], r)
            x0 += r.w + step
        