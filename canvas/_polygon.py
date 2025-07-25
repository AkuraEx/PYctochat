import pygame
from canvas._base import BaseCanvas, RGBTuple
import sys
import config as C

from pygame import Vector2, gfxdraw


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
        gfxdraw.filled_polygon(self.draw_surface, pts, self.color)
        gfxdraw.aapolygon(self.draw_surface, pts, self.color)

    def _draw_cap(self, pos: tuple[int, int]):
        if self.last_pos:
            self._draw_line(Vector2(self.last_pos), Vector2(pos))

        gfxdraw.filled_circle(
            self.draw_surface, pos[0], pos[1], self.thickness, self.color
        )
        gfxdraw.aacircle(
            self.draw_surface, pos[0], pos[1], self.thickness, self.color
        )

    def _process_events(self):
        mousePos = pygame.mouse.get_pos()
        inDrawWindow = (
            mousePos[1] < C.WINDOW_HEIGHT / 2
            and mousePos[0] < C.WINDOW_WIDTH / 2
        )
        inPostWindow = mousePos[1] > C.WINDOW_HEIGHT / 2

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    sys.exit()
                case pygame.MOUSEBUTTONUP:
                    if inDrawWindow:
                        self._draw_cap(self._pos_to_rel(event.pos))
                    elif inPostWindow:
                        self._post()
                case pygame.MOUSEBUTTONDOWN:
                    if inDrawWindow:
                        self.line_stack.push(self.__bytes__())
                        self._draw_cap(self._pos_to_rel(event.pos))
                        self.last_pos = self._pos_to_rel(event.pos)
                case _:
                    pass

        # Once per frame, update the line if the mouse is still down
        if pygame.mouse.get_pressed()[0] and inDrawWindow:
            end = Vector2(self._pos_to_rel(mousePos))
            if self.last_pos:
                start = Vector2(self.last_pos)
                self._draw_line(start, end)
            self.last_pos = end
        else:
            self.last_pos = None
            self.last_edge = None
