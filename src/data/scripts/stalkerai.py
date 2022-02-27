from tkinter.colorchooser import Chooser
from typing import List

import random

from SakuyaEngine.clock import Clock

from .window import Window


class StalkerAI:
    def __init__(
        self, windows: List[Window], choice_cooldown: float, choice_percent: float
    ) -> None:
        self.windows = windows
        self.choice_cooldown = choice_cooldown
        self.choice_percent = choice_percent

        self.clock = Clock()

    def choose(self) -> Window:
        return random.choice(self.windows)

    def update(self) -> None:
        if self.clock.get_time() >= self.choice_cooldown:
            self.clock.reset()
            if self.choice_percent >= random.random():
                return self.choose()

        return None
