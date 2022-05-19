from typing import List

import random
import pygame
import SakuyaEngine as engine

from .window import Window
from .const import OPEN_WINDOW_SOUND


class StalkerAI:
    def __init__(
        self, windows: List[Window], choice_cooldown: float, choice_percent: float, scene: engine.Scene
    ) -> None:
        self.windows = windows
        self.choice_cooldown = choice_cooldown
        self.choice_percent = choice_percent
        self.window_choice_percent = 0.5

        self.cooldown_clock = engine.Clock()
        self.runtime_clock = engine.Clock()

        self.current_window = None
        self.current_floor_break_pos = None
        self.floor_breaks = {}
        self.scene = scene

    @property
    def is_active(self) -> bool:
        return self.current_window or self.current_floor_break_pos

    def choose_window(self) -> Window:
        return random.choice(self.windows)

    def choose_floor(self) -> pygame.Vector2:
        x = self.game_map.get_width() - 1
        y = self.game_map.get_height() - 1
        
        print("d")
        return pygame.Vector2(random.choice(0, x), random.choice(0, y))

    def open_window(self, window: Window) -> None:
        self.current_window = window
        window.open_percent = 1
        OPEN_WINDOW_SOUND.play()

    def start_floor_break(self, pos: pygame.Vector2) -> None:
        self.current_floor_break_pos = pos
        self.floor_breaks[pos] = {"progress": 0}

    def update(self) -> None:
        if (
            self.cooldown_clock.get_time() >= self.choice_cooldown
            and self.is_active
        ):
            self.cooldown_clock.reset()
            if self.choice_percent >= random.random():
                
                if self.window_choice_percent >= random.random():
                    self.open_window(self.choose_window())

                else:
                    self.start_floor_break(self.choose_floor())

        return None
