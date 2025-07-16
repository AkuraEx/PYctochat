from abc import ABC, abstractmethod
import pygame

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

        pygame.init()

        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(size)

        self.clear()

    def bytes(self):
        return pygame.image.tostring(self.surface, "RGB")

    def clear(self) -> None:
        self.surface.fill(self.background)

    def do_frame(self) -> None:
        self._process_events()
        pygame.display.update()
        self.clock.tick()

    @abstractmethod
    def _process_events(self) -> None:
        pass
