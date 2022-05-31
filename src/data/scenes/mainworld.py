from data.scripts.const import *
from data.scripts.pygame_const import (
    FLOOR_BREAK_TEXTURE,
    KEYBOARD,
    MAX_FLOOR_BREAK_VAL,
)
from data.scripts.controller import PlayerController
from data.scripts.random_noise import apply_noise
from data.scripts.stalkerai import StalkerAI
from data.scripts.map_loader import GameMap
from data.scripts.map_cmds import *
from data.scripts.player import Player
from data.scripts.stalker import Stalker
from data.scripts.window import Window

import math
import pygame
import sys
import SakuyaEngine as engine

## stalker trioes to go through the floor to get into the house and the player needs to place a textbook ontop of
# the floor to prevent him from getting inside. and occasionally the player needs the textbook to complete homework


class MainWorld(engine.Scene):
    def on_awake(self):
        screen_size = pygame.Vector2(self.client.screen.get_size())

        self.draw_debug_collisions = False
        self.PX_INTERACT_MIN_DISTANCE = 15

        # Map Setup
        self.game_map = GameMap("data/tilemaps/house.tmx")
        self.lightroom = engine.LightRoom(
            self, force_size=self.game_map.surface.get_size()
        )
        self.light_collisions = []

        self.collision_rects = self.game_map.collision_rects

        for r in self.game_map.light_col_rects:
            line = engine.rect_to_lines(r)
            self.light_collisions.extend(line)

        # Player Setup
        self.player = Player()
        self.player.position = screen_size / 3
        self.add_entity(self.player)
        self.controller = PlayerController()

        # if None, textbook with player
        # if Vector, textbook on floor
        self.textbook_location = None

        self.doing_homework = False
        self.homework_progress = engine.Clock(pause_upon_start=True)
        self.homework_bar = engine.Bar(32, 4)
        self.night_progress = engine.Clock(pause_upon_start=False)

        # Load Windows
        self.windows = []
        for obj in self.game_map.data.objects:
            if obj.type and obj.visible:
                if obj.type == "window":
                    self.windows.append(
                        Window(
                            pygame.Rect(obj.x, obj.y, obj.width - 1, obj.height - 1),
                            obj.properties["window_dir"],
                        )
                    )

        # Stalker Setup
        self.stalker = Stalker()
        self.stalker.position = pygame.Vector2(-1000, -1000)
        self.add_entity(self.stalker)

        self.stalkerai = StalkerAI(self.windows, 2000, 1, self)
        self._floor_break_surf = self.game_map.surface.copy().convert_alpha()

        # Sound Setup
        self.client.sounds["white_noise"].play(repeat=True)
        self.homework_sound_channel = None

        # Font Setup
        self.font = engine.Font(
            alphabet_path="data/sprites/alphabet.png",
            numbers_path="data/sprites/numbers.png",
        )

    def input(self) -> None:
        controller = self.controller
        for event in self.events:
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
                for obj in self.game_map.interact_objs:
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
                        self.client.sounds["close_window"].play()

    @property
    def floor_break_surf(self) -> pygame.Surface:
        self._floor_break_surf.fill((0, 0, 0, 0))

        for f in self.stalkerai.floorbreak_manager.floors:
            index = f.progress_clock.get_time() / MAX_FLOOR_BREAK_VAL
            try:
                self._floor_break_surf.blit(
                    FLOOR_BREAK_TEXTURE[int(index)], f.world_pos
                )

            except IndexError:
                if index >= 5:
                    self.stalkerai.inside_house = True

        return self._floor_break_surf

    def update(self):
        screen_size = pygame.Vector2(self.client.screen.get_size())

        self.screen.fill((0, 0, 0))

        # Stalker AI
        self.stalkerai.update()

        ## Checks if Stalker got inside by Windows
        ## self.floor_break_surf() checks if Stalker
        ## got inside by floor
        for w in self.windows:
            if w.display_open_percent == 1:
                self.stalkerai.inside_house = True

        # Camera
        self.camera.position = -self.player.center_position + screen_size / 2

        # Draw Player Flashlight
        player_dir = math.degrees(
            engine.get_angle(
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

        # Draw Map & Potential Floor Breaks
        map_surf = self.game_map.surface
        map_surf.blit(self.floor_break_surf, (0, 0))
        self.screen.blit(map_surf, self.camera.position)

        # Draw & Update Windows
        for w in self.windows:
            w.draw_light(self.lightroom)
            w.update(self.client.delta_time)

        # Draw LightRoom
        self.screen.blit(self.lightroom.surface, self.camera.position)

        # Draw Interaction Hints
        for obj in self.game_map.interact_objs:
            mp = self.client.mouse_pos
            if obj["rect"].collidepoint(mp - self.camera.position):
                t = self.font.text(obj["hint"])
                self.screen.blit(
                    t, (screen_size.x / 2 - t.get_width() / 2, screen_size.y * 2 / 3)
                )

        self.player.velocity = self.player.speed * self.controller.movement

        # Draw Entities
        for e in self.entities:
            self.screen.blit(e.sprite, e.abs_position + self.camera.position)

        apply_noise(self)

        # Draw Clock
        time_val = self.night_progress.get_time()
        time_surf = self.font.text(f"{int(time_val / 1000 / 60 + 1)}AM")
        self.screen.blit(time_surf, (0, 0))

        # Homework Progress
        prog_val = self.homework_progress.get_time()
        homework_prog = int(prog_val * 10 / HOMEWORK_QUOTA)
        prog_text_surf = self.font.text(f"{homework_prog}")
        self.screen.blit(prog_text_surf, (0, 6))
        prog_text_surf_width = prog_text_surf.get_width()
        pygame.draw.rect(
            self.screen,
            (200, 200, 200),
            [prog_text_surf_width + 1, 6, self.homework_bar.max_val, 5],
        )
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            [prog_text_surf_width + 1, 6, self.homework_bar.display_val, 5],
        )
        self.homework_bar.current_val = (
            int(prog_val * 10 / HOMEWORK_QUOTA) / 100 * self.homework_bar.max_val
        )
        self.homework_bar.update(self.client.delta_time)

        if self.player.velocity.magnitude() > 0:
            self.doing_homework = False

        if self.doing_homework:
            self.homework_progress.resume()
            self.homework_sound_channel = self.client.sounds["homework_progress"].play(
                repeat=True
            )

        if not self.doing_homework:
            self.homework_progress.pause()

        # Footsteps
        if self.player.velocity.magnitude() > 0:
            self.client.sounds["footstep1"].play(repeat=True)
        else:
            self.client.sounds["footstep1"].stop()

        self.input()
        self.advance_frame()
