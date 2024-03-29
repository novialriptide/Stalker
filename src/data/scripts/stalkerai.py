from typing import List

import random
import logging
import SakuyaEngine as engine

from data.scripts.floorbreak_manager import FloorBreakManager

from .window import Window


class StalkerAI:
    def __init__(
        self,
        windows: List[Window],
        choice_cooldown: float,
        choice_percent: float,
        scene: engine.Scene,
    ) -> None:
        self.inside_house = False
        self.spawned = False
        self.init_pos = None

        self.windows = windows
        self.choice_cooldown = choice_cooldown
        self.choice_percent = choice_percent
        self.window_choice_percent = 0.5

        self.cooldown_clock = engine.Clock()

        self.current_window = None
        self.scene = scene
        self.floorbreak_manager = FloorBreakManager(self)

    @property
    def is_active(self) -> bool:
        return (
            self.current_window is not None
            or self.floorbreak_manager.current_floor is not None
        )

    def choose_window(self) -> Window:
        return random.choice(self.windows)

    def open_window(self, window: Window) -> None:
        self.current_window = window
        window.open_percent = 1

    def update(self) -> None:
        if (
            self.cooldown_clock.get_time() >= self.choice_cooldown
            and not self.is_active
        ):
            self.cooldown_clock.reset()
            if self.choice_percent >= random.random():
                logging.info("Stalker is choosing an action (Window/Floor)")
                if self.window_choice_percent >= random.random():
                    logging.info("Stalker chose window")
                    self.open_window(self.choose_window())
                    self.scene.client.sounds["open_window"].play()

                else:
                    logging.info("Stalker chose floor")
                    self.floorbreak_manager.choose_floor()
