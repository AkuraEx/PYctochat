import sys
import pygame
from pygame import gfxdraw
from pygame.event import Event
from canvas._base import BaseCanvas, RGBTuple


class NaiveCanvas(BaseCanvas):
    _mouse_down: bool

    def __init__(
        self,
        color: RGBTuple,
        background: RGBTuple,
        thickness: int,
    ) -> None:
        super().__init__(color, background, thickness)
        self._mouse_down = False

    def _circle_at_event(self, event: Event):
        x, y = event.pos
        gfxdraw.filled_circle(self.surface, x, y, self.thickness, self.color)
        gfxdraw.aacircle(self.surface, x, y, self.thickness, self.color)

    def _process_events(self) -> None:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    sys.exit()
                case pygame.MOUSEBUTTONUP:
                    self._circle_at_event(event)
                    self._mouse_down = False
                case pygame.MOUSEBUTTONDOWN:
                    self._circle_at_event(event)
                    self._mouse_down = True
                case pygame.MOUSEMOTION:
                    if self._mouse_down:
                        self._circle_at_event(event)
                case _:
                    pass
