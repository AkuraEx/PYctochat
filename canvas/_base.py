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
    post_list: list[bytes]

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
        self.post_list = []

        pygame.init()

        self.clock = pygame.time.Clock()
        self.main_display = pygame.display.set_mode(size)
        self.draw_surface = pygame.Surface(C.SCREEN)

        self.bottom_screen = pygame.transform.scale_by(
            pygame.image.load("assets/backSprite.png"), 3
        )

        self.back_drop = pygame.transform.scale_by(
            pygame.image.load("assets/backDrop.png"), 3
        )

        self.main_display.fill(self.background)
        self.draw_surface.blit(self.back_drop, (0, 0))
        self.main_display.blit(self.back_drop, (C.FRAME_WIDTH, 0))
        self.main_display.blit(
            self.back_drop, (C.SCREEN_WIDTH + C.FRAME_WIDTH, 0)
        )
        self.main_display.blit(self.bottom_screen, (C.FRAME_WIDTH, 0))
        self.clear()

    def __bytes__(self):
        return pygame.image.tobytes(self.draw_surface, "RGB")

    def _pos_to_rel(self, pos: tuple[int, int]):
        return (pos[0] - C.FRAME_WIDTH, pos[1])

    def clear(self) -> None:
        self.line_stack.reset()
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
        self.post_list.append(drawing)

        count = len(self.post_list) - 1
        for item in self.post_list:
            undone = pygame.image.frombytes(item, C.SCREEN, "RGB")
            self.main_display.blit(
                undone,
                (C.SCREEN_WIDTH + C.FRAME_WIDTH, C.SCREEN_HEIGHT * count),
            )
            count -= 1
        self.clear()

    @abstractmethod
    def _process_events(self) -> None:
        pass
