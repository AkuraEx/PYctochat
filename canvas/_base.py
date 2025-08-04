from abc import ABC, abstractmethod
import pygame
from helpers._stack import Stack
import config as C

type RGBTuple = tuple[int, int, int]


class BaseCanvas(ABC):
    color: RGBTuple
    background: RGBTuple
    thickness: int

    history: Stack[bytes]

    def __init__(
        self,
        color: RGBTuple,
        background: RGBTuple,
        thickness: int,
    ) -> None:
        self.color = color
        self.background = background
        self.thickness = thickness

        self.history = Stack()

        pygame.init()

        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode(vsync=True)
        self.surface = pygame.Surface(C.SCREEN)

        self.clear()

    def __bytes__(self):
        return pygame.image.tobytes(self.surface, "RGBA")

    def resolution(self):
        return (self.surface.get_width(), self.surface.get_height())

    def clear(self) -> None:
        self.history.reset()
        self.surface.fill((255, 255, 255, 255))

    def do_frame(self) -> None:
        self._process_events()
        self.display.blit(self.surface, (0, 0))
        pygame.display.update()
        self.clock.tick()

    def undo(self) -> None:
        if prev := self.history.pop():
            undone = pygame.image.frombytes(prev, C.SCREEN, "RGBA")
            self.surface.blit(undone, (0, 0))

    @abstractmethod
    def _process_events(self) -> None:
        pass
