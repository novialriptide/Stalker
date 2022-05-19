from typing import List

import random
import SakuyaEngine as engine

from .window import Window
from .const import OPEN_WINDOW_SOUND


class StalkerAI:
    def __init__(
        self, windows: List[Window], choice_cooldown: float, choice_percent: float
    ) -> None:
        self.windows = windows
        self.choice_cooldown = choice_cooldown
        self.choice_percent = choice_percent
        self.window_choice_percent = 0.5

        self.cooldown_clock = engine.Clock()
        self.runtime_clock = engine.Clock()

        self.current_window = None
        self.current_tile_break_pos = None

    @property
    def is_active(self) -> bool:
        return self.current_window or self.current_tile_break_pos

    def choose_window(self) -> Window:
        return random.choice(self.windows)

    def open_window(self, window: Window) -> None:
        window.open_percent = 1
        OPEN_WINDOW_SOUND.play()

    def update(self) -> None:
        if (
            self.cooldown_clock.get_time() >= self.choice_cooldown
            and self.is_active
        ):
            self.cooldown_clock.reset()
            if self.choice_percent >= random.random():
                
                if self.window_choice_percent >= random.random():
                    window_choice = self.choose_window()
                    self.current_window = window_choice
                    return self.open_window(window_choice)

                else:
                    

        return None
