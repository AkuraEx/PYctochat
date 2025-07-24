from abc import ABC, abstractmethod
import pygame
from helpers._stack import Stack
import config as C

type RGBTuple = tuple[int, int, int]


class BaseCanvas(ABC):
    color: RGBTuple
    background: RGBTuple
    thickness: int

    line_stack: Stack[bytes]
    post_stack: Stack[bytes]

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

        self.line_stack = Stack()
        self.post_stack = Stack()

        pygame.init()

        self.clock = pygame.time.Clock()
        self.main_display = pygame.display.set_mode(size)
        self.draw_surface = pygame.Surface(C.SCREEN)

        self.bottom_screen = pygame.transform.scale_by(
            pygame.image.load("assets/backSprite.png"), 3
        )

        self.clear()

    def __bytes__(self):
        return pygame.image.tobytes(self.draw_surface, "RGB")

    def clear(self) -> None:
        self.line_stack.reset()
        self.main_display.fill(self.background)
        self.main_display.blit(self.bottom_screen, (C.FRAME_WIDTH, 0))
        self.draw_surface.blit(self.bottom_screen, (0, 0))

    def do_frame(self) -> None:
        self._process_events()
        self.main_display.blit(self.draw_surface, (C.FRAME_WIDTH, 0))
        pygame.display.update()
        self.clock.tick()

    def undo(self) -> None:
        if prev := self.line_stack.pop():
            undone = pygame.image.frombytes(prev, C.SCREEN, "RGB")
            self.draw_surface.blit(undone, (0, 0))

    def _post(self) -> None:
        drawing = bytes(self)
        self.post_stack.push(drawing)
        self.clear()

        undone = pygame.image.frombytes(drawing, C.SCREEN, "RGB")
        self.main_display.blit(undone, (C.SCREEN_WIDTH + C.FRAME_WIDTH, 0))

    @abstractmethod
    def _process_events(self) -> None:
        pass
