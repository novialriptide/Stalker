from SakuyaEngine.scene import Scene
from SakuyaEngine.lights import LightRoom
from SakuyaEngine.math import get_angle

from data.scripts.map_loader import GameMap

from math import degrees

import pygame
import sys

class MainWorld(Scene):
    def on_awake(self):
        self.lightroom = LightRoom(self)
        self.collisions = [[pygame.Vector2(75, 35), pygame.Vector2(75, 75)]]
        
        self.g = GameMap("C:/Users/novia/Documents/GitHub/Stay-Alert/src/data/tilemaps/house.tmx")

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen_size = pygame.Vector2(self.client.screen.get_size())

        self.screen.fill((0, 0, 255))

        self.lightroom.draw_point_light(screen_size / 2, 35, collisions=self.collisions)

        dir = degrees(get_angle(self.client.mouse_pos, screen_size / 2)) + 180
        self.lightroom.draw_spot_light(
            screen_size / 2, 150, dir, 65, collisions=self.collisions
        )
        dir = degrees(get_angle(self.client.mouse_pos, screen_size / 3)) + 180
        self.lightroom.draw_spot_light(
            screen_size / 3, 150, dir, 45, collisions=self.collisions
        )
        self.screen.blit(self.g.surface, (0, 0))
        
        self.screen.blit(self.lightroom.surface, (0, 0))

        for c in self.collisions:
            pygame.draw.line(self.screen, (255, 0, 0), c[0], c[1])