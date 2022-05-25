from typing import List

import pygame
import SakuyaEngine as engine


class Entity(engine.Entity):
    def __init__(
        self,
        name: str = None,
        tags: List[str] = [],
        scale: float = 1,
        position: pygame.Vector2 = pygame.Vector2(0, 0),
        obey_gravity: bool = False,
        speed: float = 0,
        custom_hitbox_size: pygame.Vector2 = pygame.Vector2(0, 0),
        gravity_scale: float = 1,
    ) -> None:
        super().__init__(
            name=name,
            tags=tags,
            scale=scale,
            position=position,
            obey_gravity=obey_gravity,
            speed=speed,
            custom_hitbox_size=custom_hitbox_size,
            gravity_scale=gravity_scale,
        )
        self.gravity = pygame.Vector2(0, 0)
        self.target_position = None
