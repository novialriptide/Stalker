from data.scripts.entity import Entity

from SakuyaEngine.tile import split_image
from SakuyaEngine.animation import Animation

import pygame

class Stalker(Entity):
    def on_awake(self, scene) -> None:
        self.speed = 0.5
        self.can_walk = True

        idle = Animation(
            "idle", split_image(pygame.image.load("data/sprites/player.png"), 10, 10)
        )
        self.anim_add(idle)
        self.anim_set("idle")