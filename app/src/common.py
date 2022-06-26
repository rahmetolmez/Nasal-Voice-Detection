import pygame
import os
from menu import Menu
import random
from controller import controller as ctrl

BLOCK_SIZE = 4
WIN_WIDTH, WIN_HEIGHT = 240 * BLOCK_SIZE, 135 * BLOCK_SIZE

class common:
	#WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
	WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

CANVAS = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
CANVAS.set_alpha(0)

# game states
STATE_NORMAL = 0
STATE_FLY_CAUGHT = 1
STATE_FLY_EATEN = 2
STATE_GAME_END = 3

FPS = 60
GRAVITY = -0.9

LBLUE = (0, 200, 255)

RED = (255, 0, 77)
ORANGE = (255, 163, 0)
YELLOW = (255, 236, 39)
GREEN = (0, 228, 54)
BLUE = (41, 173, 255)
WHITE = (255, 241, 232)
BLACK = (0, 0, 0)

RAINBOW = [WHITE, GREEN]
