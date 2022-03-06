from SakuyaEngine.scene import Scene
from SakuyaEngine.lights import LightRoom
from SakuyaEngine.math import get_angle, rect_to_lines

from data.scripts.controller import PlayerController
from data.scripts.map_loader import GameMap
from data.scripts.map_cmds import CMDS
from data.scripts.player import Player
from data.scripts.const import KEYBOARD, RANDOM_NOISE, RANDOM_NOISE_SIZE
from data.scripts.window import Window
from data.scripts.stalkerai import StalkerAI
from data.scripts.random_noise import apply_noise

import math
import pygame
import sys


class Test(Scene):
    def on_awake(self):
        screen_size = pygame.Vector2(self.client.screen.get_size())

        self.collision_rects = [
            pygame.Rect(30, 30, 50, 50)
        ]

        # Player Setup
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

    def update(self):
        self.screen.fill((0, 0, 0))

        self.player.velocity = self.player.speed * self.controller.movement
        
        for c in self.collision_rects:
            pygame.draw.rect(self.screen, (255, 0, 0), c)
        
        # Draw Entities
        for e in self.entities:
            self.screen.blit(e.sprite, e.position + self.camera.position)

        self.input()
        self.advance_frame()
