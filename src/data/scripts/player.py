from SakuyaEngine.animation import Animation
from SakuyaEngine.tile import split_image
from SakuyaEngine.math import vector2_move_toward, move_toward

from .entity import Entity

from typing import List

import pygame


class Player(Entity):
    def on_awake(self) -> None:
        self.speed = 0.75

        idle = Animation(
            "idle", split_image(pygame.image.load("data/sprites/player.png"), 8, 8)
        )
        self.anim_add(idle)
        self.anim_set("idle")
        
        self.opacity = 1
        self.display_opacity = self.opacity
        self.hiding = False

    def on_update(self) -> None:
        if self.target_position is not None:
            if self.target_position == self.position:
                self.target_position = None

            elif self.target_position != self.position:
                self.position = vector2_move_toward(self.position, self.target_position, self.speed)
        
        if self.hiding:
            self.opacity = 0
        if not self.hiding:
            self.opacity = 1
        self.display_opacity = move_toward(self.display_opacity, self.opacity, 0.05)
        
        self.alpha = self.display_opacity * 255