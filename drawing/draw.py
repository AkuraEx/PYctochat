import pygame
import math


def thick_aaline(
    display: pygame.Surface,
    color: tuple[int, int, int],
    point0: tuple[int, int],
    point1: tuple[int, int],
    w: int,
) -> None:
    # Unpack individual coordinates
    x0, y0 = point0
    x1, y1 = point1

    # Find the distance between them
    dx = x1 - x0
    dy = y1 - y0
    distance = math.hypot(dx, dy)

    # If the line has no length, there's nothing to draw
    if distance == 0:
        return

    # Adjust the coordinates to create a rectangle
    proportion = w / distance / 2
    adjx = dx * proportion
    adjy = dy * proportion

    pts = (
        (x0 - adjy, y0 + adjx),  # A
        (x0 + adjy, y0 - adjx),  # B
        (x1 + adjy, y1 - adjx),  # C
        (x1 - adjy, y1 + adjx),  # D
    )

    # Draw the rectangle
    pygame.draw.aalines(display, color, True, pts, True)
    pygame.draw.polygon(display, color, pts, 0)
