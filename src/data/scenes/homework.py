import SakuyaEngine as engine
import pygame
import sys
import math
from data.scripts.pygame_const import BACKGROUND_SPRITE

"""
Your mother has left home and you have homework you must complete by 6AM.
There is a slight problem, someone is trying to get inside your home.
Keep them out.
"""


class MainTitle(engine.Scene):
    def on_awake(self, **kwargs) -> None:
        pygame.font.init()
        self.screen_size = pygame.Vector2(self.client.screen.get_size())

        self.font = engine.Font(
            alphabet_path=engine.resource_path("data/sprites/alphabet.png"),
            numbers_path=engine.resource_path("data/sprites/numbers.png"),
        )

    def input(self) -> None:
        for event in self.events:
            if event.type == pygame.QUIT:
                sys.exit()

    def update(self) -> None:
        self.input()
        self.advance_frame()
