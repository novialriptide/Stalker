from SakuyaEngine.scene import Scene
from SakuyaEngine.lights import LightRoom
from SakuyaEngine.math import get_angle, rect_to_lines
from SakuyaEngine.text import Font
from SakuyaEngine.clock import Clock

from data.scripts.const import KEYBOARD, CLOSE_WINDOW_SOUND
from data.scripts.controller import PlayerController
from data.scripts.random_noise import apply_noise
from data.scripts.stalkerai import StalkerAI
from data.scripts.map_loader import GameMap
from data.scripts.map_cmds import *
from data.scripts.player import Player
from data.scripts.window import Window

import math
import pygame
import sys


class MainWorld(Scene):
    def on_awake(self):
        screen_size = pygame.Vector2(self.client.screen.get_size())

        self.draw_debug_collisions = False
        self.PX_INTERACT_MIN_DISTANCE = 15

        # Map Setup
        self.g = GameMap("data/tilemaps/house.tmx")
        self.lightroom = LightRoom(self, size=self.g.surface.get_size())
        self.light_collisions = []

        self.collision_rects = self.g.collision_rects

        for r in self.g.light_col_rects:
            line = rect_to_lines(r)
            self.light_collisions.extend(line)

        # Player Setup
        self.player = Player()
        self.player.position = screen_size / 3
        self.add_entity(self.player)
        self.controller = PlayerController()
        self.homework_quota = 25000
        self.doing_homework = False
        self.homework_progress = Clock(pause_upon_start = True)
        self.night_progress = Clock(pause_upon_start = False)

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
        self.stalkerai = StalkerAI(self.windows, 2000, 0.1)

        # Font Setup
        self.font = Font(alphabet_path="data/sprites/alphabet.png", numbers_path="data/sprites/numbers.png")

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

                    if event.key == KEYBOARD["right1"]:
                        controller.is_moving_right = False

                    if event.key == KEYBOARD["up1"]:
                        controller.is_moving_up = False

                    if event.key == KEYBOARD["down1"]:
                        controller.is_moving_down = False

                if event.key == KEYBOARD["select"]:
                    self.client.add_scene("Pause", exit_scene=self)
                    self.pause()

            if event.type == pygame.MOUSEBUTTONUP:
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
                        CMDS[obj["cmd"]](player=self.player, rect=rect, scene=self)

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
                        and w.open_percent > 0
                    ):
                        close_window(player=self.player, rect=rect, window=w)
                        self.stalkerai.current_window = None
                        CLOSE_WINDOW_SOUND.play()

    def update(self):
        screen_size = pygame.Vector2(self.client.screen.get_size())

        self.screen.fill((0, 0, 0))

        # Stalker AI
        window_choice = self.stalkerai.update()
        if window_choice is not None:
            print(f"open window {window_choice}")

        # Camera
        self.camera.position = -self.player.center_position + screen_size / 2

        # Draw Player Flashlight
        player_dir = math.degrees(
            get_angle(
                self.player.center_position + self.camera.position,
                self.client.mouse_pos,
            )
        )
        if self.player.flashlight:
            self.lightroom.draw_spot_light(
                self.player.center_position,
                60,
                player_dir,
                70,
                collisions=self.light_collisions,
                color=(166, 255, 0, 25),
            )
            self.lightroom.draw_point_light(
                self.player.center_position,
                15,
                collisions=self.light_collisions,
                color=(166, 255, 0, 25),
            )

        self.player.angle = player_dir + 90

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
                t = self.font.text(obj["hint"])
                self.screen.blit(t, (screen_size.x / 2 - t.get_width() / 2, screen_size.y * 2 / 3))

        self.player.velocity = self.player.speed * self.controller.movement

        # Draw Entities
        for e in self.entities:
            self.screen.blit(e.sprite, e.abs_position + self.camera.position)

        apply_noise(self)
        
        # Draw Clock
        time_val = self.night_progress.get_time()
        time_surf = self.font.text(f"{int(time_val / 1000 / 60 + 1)} AM")
        self.screen.blit(time_surf, (0, 0))
        
        # Homework Progress
        time_val = self.homework_progress.get_time()
        time_surf = self.font.text(f"{int(time_val * 10 / self.homework_quota)}") # make this into a bar
        self.screen.blit(time_surf, (0, 5))
        
        if self.player.velocity.magnitude() > 0:
            self.doing_homework = False
        
        if self.doing_homework:
            self.homework_progress.resume()

        if not self.doing_homework:
            self.homework_progress.pause()

        # Debug Collisions
        if self.draw_debug_collisions:
            for r in self.collision_rects:
                pygame.draw.rect(self.screen, (255, 255, 0), r)

            for c in self.light_collisions:
                pygame.draw.line(self.screen, (255, 0, 0), c[0], c[1])

            for w in self.windows:
                pygame.draw.rect(self.screen, (255, 0, 0), w.rect)

        self.input()
        self.advance_frame()
