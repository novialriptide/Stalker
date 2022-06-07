from data.scripts.entity import Entity

import pygame
import SakuyaEngine as engine


class Stalker(Entity):
    def on_awake(self, scene) -> None:
        self.speed = 0.5
        self.can_walk = True

        idle = engine.Animation(
            "idle",
            engine.split_image(pygame.image.load(engine.resource_path("data/sprites/player.png")), 10, 10),
        )
        self.anim_add(idle)
        self.anim_set("idle")
