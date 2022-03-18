from SakuyaEngine.animation import Animation
from SakuyaEngine.tile import split_image
from SakuyaEngine.math import move_toward
from SakuyaEngine.clock import Clock

from .entity import Entity

from typing import List

import pygame


class Player(Entity):
    def on_awake(self, scene) -> None:
        self.speed = 0.75
        self.can_walk = True

        idle = Animation(
            "idle", split_image(pygame.image.load("data/sprites/player.png"), 10, 10)
        )
        self.anim_add(idle)
        self.anim_set("idle")

        self.opacity = 1
        self.display_opacity = self.opacity
        self.hiding = False
        self.back_hide_pos = None
        self.flashlight = True

        self.hide_cooldown_clock = Clock()
        self.hide_cooldown_val = 2500

    def on_update(self, scene) -> None:
        if self.hiding:
            self.opacity = 0
            self.flashlight = False
            self.can_walk = False
        if not self.hiding:
            self.opacity = 1
            self.flashlight = True
            self.target_position = self.back_hide_pos
            self.can_walk = True

        if self.target_position is not None:
            if self.target_position == self.position:
                self.target_position = None

            elif self.target_position != self.position:
                self.position.move_towards_ip(self.target_position, self.speed)

        self.display_opacity = move_toward(
            self.display_opacity, self.opacity, 0.05 * scene.client.delta_time
        )

        self.alpha = self.display_opacity * 255
