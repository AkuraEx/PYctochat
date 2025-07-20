from abc import ABC, abstractmethod
import pygame
from helpers._stack import Stack

type RGBTuple = tuple[int, int, int]

class BaseCanvas(ABC):
    color: RGBTuple
    background: RGBTuple
    thickness: int

    def __init__(
        self,
        size: tuple[int, int],
        color: RGBTuple,
        background: RGBTuple,
        thickness: int,
    ) -> None:
        self.color = color
        self.background = background
        self.thickness = thickness
        self.stack = Stack()

        pygame.init()

        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(size)

        self.clear()

    def bytes(self):
        return pygame.image.tobytes(self.surface, "RGB")

    def clear(self) -> None:
        self.surface.fill(self.background)
        self.stack.reset()

    def do_frame(self) -> None:
        self._process_events()
        pygame.display.update()
        self.clock.tick()

    def _undo(self):
        if not self.stack.empty():
            undone = pygame.image.frombytes(self.stack.pop(), (576, 576), "RGB")
            self.surface.blit(undone, (0, 0))

    @abstractmethod
    def _process_events(self) -> None:
        pass
