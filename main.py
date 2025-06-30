import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

class Alien(pg.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

class Bullet(pg.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

class Bomb(pg.sprite.Sprite):
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

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
