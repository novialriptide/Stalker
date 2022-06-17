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
        self.start_text = self.font.text("START")
        self.start_text_rect = self.start_text.get_rect()
        self.start_text_rect.topleft = self.screen_size / 2 + pygame.Vector2(-48, 15)
        self.start_button = engine.Button(self.start_text_rect, method=self.on_start)
        self.button_offset = pygame.Vector2(0, 0)

    def on_start(self) -> None:
        self.client.add_scene("MainWorld")
        self.client.remove_scene("MainTitle")

    def input(self) -> None:
        for event in self.events:
            if event.type == pygame.QUIT:
                sys.exit()

    def update(self) -> None:
        self.screen.blit(BACKGROUND_SPRITE, (0, 0))
        self.screen.blit(
            self.start_text, self.start_text_rect.topleft + self.button_offset
        )
        self.start_button.update(self.client)

        self.button_offset = pygame.Vector2(0, math.sin(self.clock.get_time() / 500))

        self.input()
        self.advance_frame()
