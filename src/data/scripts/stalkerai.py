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
        self.window_choice_percent = 0

        self.cooldown_clock = engine.Clock()
        self.runtime_clock = engine.Clock()

        self.current_window = None
        self.current_floor_break_pos = None
        self.floor_breaks = []
        self.scene = scene

    @property
    def is_active(self) -> bool:
        return self.current_window is not None or self.current_floor_break_pos is not None

    def choose_window(self) -> Window:
        return random.choice(self.windows)

    def choose_floor(self) -> pygame.Vector2:
        data = self.scene.game_map.data
        x = (data.width - 1)
        y = (data.height - 1)
        rand_pos = pygame.Vector2(random.randint(0, x) * data.tilewidth, random.randint(0, y) * data.tileheight)

        for r in self.scene.collision_rects:
            if r.collidepoint(rand_pos):
                return                

        return rand_pos

    def open_window(self, window: Window) -> None:
        self.current_window = window
        window.open_percent = 1
        OPEN_WINDOW_SOUND.play()

    def start_floor_break(self, pos: pygame.Vector2) -> None:
        if pos is None:
            return
        
        self.current_floor_break_pos = pos
        self.floor_breaks.append({"progress": 0, "pos": pos})

    def update(self) -> None:
        if (
            self.cooldown_clock.get_time() >= self.choice_cooldown
            and not self.is_active
        ):
            self.cooldown_clock.reset()
            if self.choice_percent >= random.random():
                if self.window_choice_percent >= random.random():
                    self.open_window(self.choose_window())

                else:
                    self.start_floor_break(self.choose_floor())

