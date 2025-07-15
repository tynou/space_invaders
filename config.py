from powerup_types import PowerupTypes

import pygame as pg

WORLD_SIZE = (400, 500)
SCORE_POS = (5, 5)

UPDATE_PERIOD = 5

STARTING_POS = (WORLD_SIZE[0] // 2, WORLD_SIZE[1] * 9 // 10)
SPACESHIP_SPEED = 100
FIRE_INTERVAL = 500
BULLET_SPEED = 500
POWERUP_SPEED = 100
EXPLOSION_DURATION = 10
SPRITE_SHIFT_PERIOD = 200
ALIEN_FORMATION = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
ALIEN_FORMATION_WIDTH = 340
ALIEN_STARTING_Y = WORLD_SIZE[1] * 3 // 10
ALIEN_SPEED = 10
LASER_SPEED = 200
LASER_FIRING_PERIOD = 1000
BUNKER_POSITIONS = [
    ((WORLD_SIZE[0] // 18) + (WORLD_SIZE[0] // 9 * 1), WORLD_SIZE[1] * 8 // 10),
    ((WORLD_SIZE[0] // 18) + (WORLD_SIZE[0] // 9 * 3), WORLD_SIZE[1] * 8 // 10),
    ((WORLD_SIZE[0] // 18) + (WORLD_SIZE[0] // 9 * 5), WORLD_SIZE[1] * 8 // 10),
    ((WORLD_SIZE[0] // 18) + (WORLD_SIZE[0] // 9 * 7), WORLD_SIZE[1] * 8 // 10)
]
BUNKER_EXPLOSION_RADIUS = 4
BUNKER_DESTRUCTION_PROBABILITY = 0.8

LIVES_POS = (10, WORLD_SIZE[1] - 20)

pg.init()
COLOR_INACTIVE = pg.Color(150, 150, 255)
COLOR_ACTIVE = pg.Color(200, 200, 255)
FONT = pg.font.SysFont(None, 32)

COLOR_WHITE = pg.Color(255, 255, 255)

LEADERBOARD_FILE_PATH = "./data/leaderboard.txt"

MYSTERY_SHIP_SPEED = 100
MYSTERY_SHIP_STARTING_Y = 50
MYSTERY_SHIP_PERIOD = 20000

SPRITE_PATH = "./sprites/"
SOUND_PATH = "./sounds/"

POWERUP_SPRITES = {
    PowerupTypes.HEALTH: "health_powerup.png",
    PowerupTypes.TRIPLE_SHOT: "bullet_powerup.png",
    PowerupTypes.SHIELD: "shield_powerup.png",
}

POWERUP_DROP_CHANCE = 0.1