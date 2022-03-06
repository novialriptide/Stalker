from tkinter.colorchooser import Chooser
from typing import List

import random

from SakuyaEngine.clock import Clock

from .window import Window
from .const import OPEN_WINDOW_SOUND


class StalkerAI:
    def __init__(
        self, windows: List[Window], choice_cooldown: float, choice_percent: float
    ) -> None:
        self.windows = windows
        self.choice_cooldown = choice_cooldown
        self.choice_percent = choice_percent

        self.cooldown_clock = Clock()
        self.runtime_clock = Clock()
        
        self.current_window = None

    def choose(self) -> Window:
        return random.choice(self.windows)
    
    def open_window(self, window: Window) -> None:
        window.open_percent = 1
        OPEN_WINDOW_SOUND.play()

    def update(self) -> None:
        if self.cooldown_clock.get_time() >= self.choice_cooldown and self.current_window is None:
            self.cooldown_clock.reset()
            if self.choice_percent >= random.random():
                window_choice = self.choose()
                self.current_window = window_choice
                return self.open_window(window_choice)

        return None
