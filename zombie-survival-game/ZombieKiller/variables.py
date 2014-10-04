#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math, pygame
import progress

MAP_WIDTH, MAP_HEIGHT = 1280, 768
WIDTH, HEIGHT = MAP_WIDTH, MAP_HEIGHT
TILE_SIZE = 256
FPS = 30

FLAGS = 0

GRAD = math.pi / 180

PLAYER_SPEED = 5.0
BULLET_VELOCITY = 26.0
directions = {'n': 0, 's': 180, 'e': 270, 'w': 90}

PISTOL, SHOTGUN, AUTOMATIC, BAZOOKA, GRENADE = 0, 1, 2, 3, 4
SURVIVOR_HEALTH = 100

player_progress = progress.GameProgress()
