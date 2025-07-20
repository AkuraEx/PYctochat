import pygame
from canvas._base import BaseCanvas, RGBTuple
import sys
from helpers._stack import Stack
import config as C

from pygame import Vector2, gfxdraw
from pygame.locals import *


class PolygonCanvas(BaseCanvas):
    def __init__(
        self,
        size: tuple[int, int],
        color: RGBTuple,
        background: RGBTuple,
        thickness: int,
    ) -> None:
        super().__init__(size, color, background, thickness)
    

    def _draw_line(self, start: Vector2, end: Vector2):
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

    def _draw_cap(self, pos: tuple[int, int]):
        if self.last_pos:
            self._draw_line(Vector2(self.last_pos), Vector2(pos))

        gfxdraw.filled_circle(
            self.surface, pos[0], pos[1], self.thickness, self.color
        )
        gfxdraw.aacircle(
            self.surface, pos[0], pos[1], self.thickness, self.color
        )

    

    def _process_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    sys.exit()
                case pygame.MOUSEBUTTONUP:
                    self._draw_cap(event.pos)
                case pygame.MOUSEBUTTONDOWN:
                    self.stack.push(self.bytes())
                    self._draw_cap(event.pos)
                    self.last_pos = event.pos
                case _:
                    pass
        


        # Once per frame, update the line if the mouse is still down
        if pygame.mouse.get_pressed()[0]:
            end = Vector2(pygame.mouse.get_pos())
            if self.last_pos:
                start = Vector2(self.last_pos)
                self._draw_line(start, end)
            self.last_pos = end
        else:
            self.last_pos = None
            self.last_edge = None
