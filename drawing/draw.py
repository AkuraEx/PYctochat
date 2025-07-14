import pygame
from pygame.locals import *
import math
from config import *


def thick_aaline(display, color, point0, point1, w):
    x0, y0 = point0
    x1, y1 = point1
    dx = x1 - x0
    dy = y1 - y0
    distance = math.hypot(dx, dy)

    if distance == 0:
        return

    proportion = w / distance / 2
    adjx = dx * proportion
    adjy = dy * proportion

    pts = (
        (x0 - adjy, y0 + adjx),  # A
        (x0 + adjy, y0 - adjx),  # B
        (x1 + adjy, y1 - adjx),  # C
        (x1 - adjy, y1 + adjx),
    )  # D

    pygame.draw.aalines(display, color, True, pts, True)
    pygame.draw.polygon(display, color, pts, 0)
