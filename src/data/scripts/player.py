from .entity import Entity

from typing import List

import pygame


class Player(Entity):
    def __init__(
        self,
        name: str = None,
        tags: List[str] = [],
        scale: float = 1,
        position: pygame.Vector2 = pygame.Vector2(0, 0),
        obey_gravity: bool = False,
        speed: float = 0.5,
        custom_hitbox_size: pygame.Vector2 = pygame.Vector2(0, 0),
        gravity_scale: float = 0,
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

    def on_update(self) -> None:
        print("d")
