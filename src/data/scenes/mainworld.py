from SakuyaEngine.scene import Scene
from SakuyaEngine.lights import LightRoom
from SakuyaEngine.math import get_angle, rect_to_lines

from data.scripts.controller import PlayerController
from data.scripts.map_loader import GameMap
from data.scripts.map_cmds import CMDS
from data.scripts.player import Player
from data.scripts.const import KEYBOARD
from data.scripts.window import Window
from data.scripts.stalkerai import StalkerAI

import math
import pygame
import sys


class MainWorld(Scene):
    def on_awake(self):
        screen_size = pygame.Vector2(self.client.screen.get_size())

        self.draw_debug_collisions = False
        self.PX_INTERACT_MIN_DISTANCE = 15

        # Map Setup
        self.lightroom = LightRoom(self)
        self.light_collisions = []

        self.g = GameMap("data/tilemaps/house.tmx")

        for r in self.g.collision_rects:
            self.collision_rects.append(r)

        for r in self.g.light_col_rects:
            line = rect_to_lines(r)
            self.light_collisions.extend(line)

        # Player Setup
        self.player = Player()
        self.player.position = screen_size / 3
        self.add_entity(self.player)
        self.controller = PlayerController()

        # Load Windows
        self.windows = []
        for obj in self.g.data.objects:
            if obj.type and obj.visible:
                if obj.type == "window":
                    self.windows.append(
                        Window(
                            pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                            obj.properties["window_dir"],
                        )
                    )

        # Stalker Setup
        self.stalkerai = StalkerAI(self.windows, 2000, 0.2)

    def input(self) -> None:
        controller = self.controller
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.player.can_walk:
                    if event.key == KEYBOARD["left1"]:
                        controller.is_moving_left = True

                    if event.key == KEYBOARD["right1"]:
                        controller.is_moving_right = True

                    if event.key == KEYBOARD["up1"]:
                        controller.is_moving_up = True

                    if event.key == KEYBOARD["down1"]:
                        controller.is_moving_down = True

            if event.type == pygame.KEYUP:
                if self.player.can_walk:
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

            if event.type == pygame.MOUSEBUTTONUP:
                # Escape hide mode
                if self.player.hiding:
                    self.player.hide_cooldown_clock.reset()
                    self.player.hiding = False

                # Player Interactions
                for obj in self.g.interact_objs:
                    rect = obj["rect"]
                    player_pos = self.player.center_position
                    dist = math.sqrt(
                        ((rect.y + rect.height / 2 - player_pos.y) ** 2)
                        + ((rect.x + rect.width / 2 - player_pos.x) ** 2)
                    )
                    if (
                        rect.collidepoint(self.client.mouse_pos - self.camera.position)
                        and dist <= self.PX_INTERACT_MIN_DISTANCE
                    ):
                        CMDS[obj["cmd"]](player=self.player, rect=rect)

                for w in self.windows:
                    rect = w.rect
                    player_pos = self.player.center_position
                    dist = math.sqrt(
                        ((rect.y + rect.height / 2 - player_pos.y) ** 2)
                        + ((rect.x + rect.width / 2 - player_pos.x) ** 2)
                    )
                    if (
                        rect.collidepoint(self.client.mouse_pos - self.camera.position)
                        and dist <= self.PX_INTERACT_MIN_DISTANCE
                    ):
                        CMDS["close_win"](player=self.player, rect=rect, window=w)

    def update(self):
        self.input()

        screen_size = pygame.Vector2(self.client.screen.get_size())

        self.screen.fill((0, 0, 0))

        # Stalker AI
        window_choice = self.stalkerai.update()

        # Camera
        self.camera.position = -self.player.center_position + screen_size / 2

        # Draw Player Flashlight
        if self.player.flashlight:
            dir = math.degrees(
                get_angle(
                    self.player.position + self.camera.position, self.client.mouse_pos
                )
            )
            self.lightroom.draw_spot_light(
                self.player.center_position,
                60,
                dir,
                70,
                collisions=self.light_collisions,
            )
            self.lightroom.draw_point_light(
                self.player.center_position + pygame.Vector2(1, 1),
                15,
                collisions=self.light_collisions,
            )

        # Draw Map
        map_surf = self.g.surface
        map_surf_size = self.g.size
        self.screen.blit(map_surf, self.camera.position)

        # Draw & Update Windows
        for w in self.windows:
            w.draw_light(self.lightroom)
            w.update(self.client.delta_time)

        # Draw LightRoom
        self.screen.blit(self.lightroom.surface, self.camera.position)

        # Draw Interaction Hints
        for obj in self.g.interact_objs:
            mp = self.client.mouse_pos
            if obj["rect"].collidepoint(mp - self.camera.position):
                pygame.draw.rect(self.screen, (255, 255, 255), (mp.x, mp.y, 17, 6))

        self.player.velocity = self.player.speed * self.controller.movement

        # Draw Entities
        for e in self.entities:
            self.screen.blit(e.sprite, e.position + self.camera.position)

        # Debug Collisions
        if self.draw_debug_collisions:
            for r in self.collision_rects:
                pygame.draw.rect(self.screen, (255, 255, 0), r)

            for c in self.light_collisions:
                pygame.draw.line(self.screen, (255, 0, 0), c[0], c[1])

            for w in self.windows:
                pygame.draw.rect(self.screen, (255, 0, 0), w.rect)

        self.advance_frame()
