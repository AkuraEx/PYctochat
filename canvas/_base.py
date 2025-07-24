from abc import ABC, abstractmethod
import pygame
from helpers._stack import Stack
import os
import config as C

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
        self.lineStack = Stack()
        self.postStack = Stack()

        pygame.init()

        self.clock = pygame.time.Clock()
        self.mainDisplay = pygame.display.set_mode(size)
        self.drawSurface = pygame.Surface((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))

        self.bottomScreen = pygame.transform.scale_by(pygame.image.load('assets/backSprite.png'), 3)

        self.clear()


    def bytes(self):
        return pygame.image.tobytes(self.drawSurface, "RGB")

    def clear(self) -> None:
        self.lineStack.reset()
        self.mainDisplay.fill(self.background)
        self.mainDisplay.blit(self.bottomScreen, (C.FRAME_WIDTH, 0))
        self.drawSurface.blit(self.bottomScreen, (0, 0))

    def do_frame(self) -> None:
        self._process_events()
        self.mainDisplay.blit(self.drawSurface, (C.FRAME_WIDTH, 0))
        pygame.display.update()
        self.clock.tick()

    def _undo(self):
        if not self.lineStack.empty():
            undone = pygame.image.frombytes(self.lineStack.pop(), (C.SCREEN_WIDTH, C.SCREEN_HEIGHT), "RGB")
            self.drawSurface.blit(undone, (0, 0))
    
    def _post(self):
        drawing = self.bytes()
        self.postStack.push(drawing)
        self.clear()
        undone = pygame.image.frombytes(self.postStack.top(), (C.SCREEN_WIDTH, C.SCREEN_HEIGHT), "RGB")
        self.mainDisplay.blit(undone, (C.SCREEN_WIDTH + C.FRAME_WIDTH, 0))


    @abstractmethod
    def _process_events(self) -> None:
        pass
