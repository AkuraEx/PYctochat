import pygame
import config as C
import sys

from pygame import Vector2, gfxdraw


class Canvas:
    color: tuple[int, int, int]

    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()

        self.surface = pygame.display.set_mode(C.CANVAS)
        self.clear()

        self.thickness = C.LINE_THICKNESS
        self.color = C.BLACK

        self.mouse_down = False

    def clear(self):
        self.surface.fill(C.WHITE)

    def draw_line(self, start: Vector2, end: Vector2):
        if start == end:
            return

        # This gets us an offset from each endpoint to construct the edge
        offset = (start - end).rotate(90).normalize() * self.thickness

        # The end edge is easy, but we have to check if we can use the
        # previous segment's end edge for the new start edge
        end_edge = (end - offset, end + offset)
        start_edge = self.last_edge or (start + offset, start - offset)

        # We have to flip the order to draw the new polygon correctly
        self.last_edge = (end_edge[1], end_edge[0])

        # Combine the edges to get a list of points
        pts = start_edge + end_edge

        # Draw the rectangle
        gfxdraw.filled_polygon(self.surface, pts, self.color)
        gfxdraw.aapolygon(self.surface, pts, self.color)

    def _draw_cap(self):
        pos = pygame.mouse.get_pos()
        gfxdraw.filled_circle(
            self.surface, pos[0], pos[1], self.thickness, self.color
        )
        gfxdraw.aacircle(
            self.surface, pos[0], pos[1], self.thickness, self.color
        )

    def do_frame(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    sys.exit()
                case pygame.MOUSEBUTTONUP:
                    self.mouse_down = False
                    self._draw_cap()
                case pygame.MOUSEBUTTONDOWN:
                    self.mouse_down = True
                    self._draw_cap()
                case _:
                    pass

            if self.mouse_down:
                end = pygame.mouse.get_pos()
                if self.last_pos:
                    start = self.last_pos
                    self.draw_line(Vector2(start), Vector2(end))
                self.last_pos = end
            else:
                self.last_pos = None
                self.last_edge = None

        pygame.display.update()
        self.clock.tick()
