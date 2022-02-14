from SakuyaEngine.scene import Scene
from SakuyaEngine.lights import LightRoom
from SakuyaEngine.math import get_angle, rect_to_lines

from data.scripts.controller import PlayerController
from data.scripts.map_loader import GameMap
from data.scripts.player import Player
from data.scripts.const import KEYBOARD

from math import degrees

import pygame
import sys


class MainWorld(Scene):
    def on_awake(self):
        self.draw_debug_collisions = False

        screen_size = pygame.Vector2(self.client.screen.get_size())
        self.lightroom = LightRoom(self)
        self.light_collisions = []

        self.g = GameMap("data/tilemaps/house.tmx")

        for r in self.g.collision_rects:
            line = rect_to_lines(r)
            self.light_collisions.extend(line)
            self.collision_rects.append(r)

        self.player = Player()
        self.player.position = screen_size / 3
        self.add_entity(self.player)

        self.controller = PlayerController()

    def input(self) -> None:
        controller = self.controller
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == KEYBOARD["left1"]:
                    controller.is_moving_left = True
                if event.key == KEYBOARD["right1"]:
                    controller.is_moving_right = True
                if event.key == KEYBOARD["up1"]:
                    controller.is_moving_up = True
                if event.key == KEYBOARD["down1"]:
                    controller.is_moving_down = True
            if event.type == pygame.KEYUP:
                if event.key == KEYBOARD["left1"]:
                    controller.is_moving_left = False
                    self.player.velocity.x = 0
                if event.key == KEYBOARD["right1"]:
                    controller.is_moving_right = False
                    self.player.velocity.x = 0
                if event.key == KEYBOARD["up1"]:
                    controller.is_moving_up = False
                    self.player.velocity.y = 0
                if event.key == KEYBOARD["down1"]:
                    controller.is_moving_down = False
                    self.player.velocity.y = 0
                if event.key == KEYBOARD["select"]:
                    self.client.add_scene("Pause", exit_scene=self)
                    self.pause()

    def update(self):
        self.input()

        screen_size = pygame.Vector2(self.client.screen.get_size())

        self.screen.fill((0, 0, 255))

        dir = degrees(get_angle(self.player.position, self.client.mouse_pos))
        self.lightroom.draw_spot_light(
            self.player.center_position, 150, dir, 70, collisions=self.light_collisions
        )
        self.lightroom.draw_point_light(
            self.player.center_position, 14, collisions=self.light_collisions
        )
        map_surf = self.g.surface
        map_surf_size = self.g.size
        self.screen.blit(map_surf, (0, 0))
        self.screen.blit(self.lightroom.surface, (0, 0))

        # Camera
        self.camera.position = pygame.Vector2(
            screen_size.x / 2 - map_surf_size.x / 2,
            screen_size.y / 2 - map_surf_size.y / 2,
        )

        self.player.velocity = self.player.speed * self.controller.movement

        for e in self.entities:
            self.screen.blit(e.sprite, e.position)

        if self.draw_debug_collisions:
            for r in self.collision_rects:
                pygame.draw.rect(self.screen, (255, 255, 0), r)

            for c in self.light_collisions:
                pygame.draw.line(self.screen, (255, 0, 0), c[0], c[1])

        self.advance_frame()
