from abc import ABC, abstractmethod
import pygame
from collections import deque
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
        self.scroll_distance = 0

        self.line_stack = Stack()
        self.post_list = deque([])

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

        self.welcome = pygame.transform.scale_by(
            pygame.image.load("assets/welcome.png"), 3
        )

        # Welcome Message on Bootup
        self.post_list.appendleft((pygame.image.tobytes(self.welcome, "RGB"), (702, 66)))

        self.main_display.fill(self.background)
        self.draw_surface.blit(self.back_drop, (0, 0))
        self.main_display.blit(self.back_drop, (C.FRAME_WIDTH, 0))
        self.main_display.blit(
            self.back_drop, (C.SCREEN_WIDTH + C.FRAME_WIDTH, 0)
        )
        self.main_display.blit(self.bottom_screen, (C.FRAME_WIDTH, 0))
        self.clear()
        self.draw_posts()

    def __bytes__(self):
        return pygame.image.tobytes(self.draw_surface, "RGB")

    def _pos_to_rel(self, pos: tuple[int, int]):
        return (pos[0] - C.FRAME_WIDTH, pos[1])

    def clear(self) -> None:
        self.line_stack.reset()
        self.main_display.blit(self.back_drop, (C.FRAME_WIDTH + C.SCREEN_WIDTH, 0))
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

    def draw_posts(self) -> None:
        n = len(self.post_list) - 1
        count = n + 1
        x_pos = C.SCREEN_WIDTH + C.FRAME_WIDTH
        y_pos = C.CANVAS_HEIGHT + self.scroll_distance
        self.clear()
        # item [0] is the drawing, item [1] is a tuple of its size so we 
        # can have varying post sizes
        for item in self.post_list:
            undone = pygame.image.frombytes(item[0], item[1], "RGB")
            # item [1][1] is the height of the image
            y_pos -= item[1][1]
            if C.CANVAS_HEIGHT > y_pos:
                self.main_display.blit(
                    undone,
                    (x_pos, y_pos),
                )
            count += 1
    

    @abstractmethod
    def _process_events(self) -> None:
        pass
