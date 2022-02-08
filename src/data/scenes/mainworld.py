from SakuyaEngine.scene import Scene
from SakuyaEngine.lights import LightRoom
from SakuyaEngine.math import get_angle, rect_to_lines

from data.scripts.map_loader import GameMap

from math import degrees

import pygame
import sys


class MainWorld(Scene):
    def on_awake(self):
        self.lightroom = LightRoom(self)
        self.light_collisions = []

        self.g = GameMap(
            "data/tilemaps/house.tmx"
        )

        for r in self.g.collision_rects:
            line = rect_to_lines(r)
            self.light_collisions.extend(line)
            self.collision_rects.append(r)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen_size = pygame.Vector2(self.client.screen.get_size())

        self.screen.fill((0, 0, 255))

        dir = degrees(get_angle(self.client.mouse_pos, screen_size / 3)) + 180
        self.lightroom.draw_spot_light(
            screen_size / 3, 150, dir, 70, collisions=self.light_collisions
        )
        map_surf = self.g.surface
        map_surf_size = self.g.size
        self.screen.blit(map_surf, (0, 0))
        self.screen.blit(self.lightroom.surface, (0, 0))

        for c in self.light_collisions:
            pygame.draw.line(self.screen, (255, 0, 0), c[0], c[1])

        # Camera
        self.camera.position = pygame.Vector2(
            screen_size.x / 2 - map_surf_size.x / 2,
            screen_size.y / 2 - map_surf_size.y / 2,
        )
