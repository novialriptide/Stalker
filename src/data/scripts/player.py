from SakuyaEngine.animation import Animation
from SakuyaEngine.tile import split_image

from .entity import Entity

from typing import List

import pygame


class Player(Entity):
    def on_awake(self) -> None:
        self.speed = 0.75
        
        idle = Animation("idle", split_image(pygame.image.load("data/sprites/player.png"), 8, 8))
        self.anim_add(idle)
        self.anim_set("idle")

    def on_update(self) -> None:
        pass
