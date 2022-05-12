import pygame
import SakuyaEngine as engine


class Window:
    def __init__(
        self,
        rect,
        window_dir,
        opening_dir: int = 1,
    ) -> None:
        self.rect = rect
        self.window_dir = window_dir
        self.opening_dir = opening_dir  # 1 is right, -1 is left

        self.open_percent = 0
        self.default_speed = 0.1
        self.close_speed = 0.1
        self.open_speed = 0.001
        self.display_open_percent = self.open_percent

    @property
    def light_length(self) -> None:
        possible_points = {
            "down": self.rect.height,
            "up": self.rect.height,
            "right": self.rect.width,
            "left": self.rect.width,
        }

        return possible_points[self.window_dir]

    @property
    def light_dir(self) -> None:
        possible_points = {"down": 90, "up": -90, "right": 0, "left": 180}

        return possible_points[self.window_dir]

    @property
    def area_light_points(self):
        possible_points = {
            "down": [
                pygame.Vector2(self.rect.x, self.rect.y),
                pygame.Vector2(self.rect.x + self.rect.width, self.rect.y),
            ],
            "up": [
                pygame.Vector2(self.rect.x, self.rect.y + self.rect.height),
                pygame.Vector2(
                    self.rect.x + self.rect.width, self.rect.y + self.rect.height
                ),
            ],
            "right": [
                pygame.Vector2(self.rect.x, self.rect.y),
                pygame.Vector2(self.rect.x, self.rect.y + self.rect.height),
            ],
            "left": [
                pygame.Vector2(self.rect.x + self.rect.width, self.rect.y),
                pygame.Vector2(
                    self.rect.x + self.rect.width, self.rect.y + self.rect.height
                ),
            ],
        }

        return possible_points[self.window_dir]

    def draw_light(self, lightroom) -> None:
        points = self.area_light_points
        open_length = (points[1] - points[0]) * self.display_open_percent
        if open_length != [0, 0]:
            lightroom.draw_area_light(
                points[0],
                points[0] + open_length,
                self.light_length,
                float(self.light_dir),
            )

    def update(self, delta_time: float) -> None:
        speed = self.open_speed
        if self.display_open_percent - self.open_percent > 0:
            speed = self.close_speed

        self.display_open_percent = engine.move_toward(
            self.display_open_percent, self.open_percent, speed * delta_time
        )
