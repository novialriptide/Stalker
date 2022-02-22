import pygame


class Window:
    def __init__(
        self,
        rect,
        light_length,
        light_dir,
        window_dir,
    ) -> None:
        self.rect = rect
        self.light_length = light_length
        self.light_dir = light_dir
        self.window_dir = window_dir

    @property
    def area_light_points(self):
        possible_points = {
            "up": [
                pygame.Vector2(self.rect.x, self.rect.y),
                pygame.Vector2(self.rect.x + self.rect.width, self.rect.y),
            ],
            "down": [
                pygame.Vector2(self.rect.x, self.rect.y + self.rect.height),
                pygame.Vector2(
                    self.rect.x + self.rect.width, self.rect.y + self.rect.height
                ),
            ],
            "left": [
                pygame.Vector2(self.rect.x, self.rect.y),
                pygame.Vector2(self.rect.x, self.rect.y + self.rect.height),
            ],
            "right": [
                pygame.Vector2(self.rect.x + self.rect.width, self.rect.y),
                pygame.Vector2(
                    self.rect.x + self.rect.width, self.rect.y + self.rect.height
                ),
            ]
            
        }
        
        return possible_points[self.window_dir]

    def draw_light(self, lightroom):
        points = self.area_light_points
        lightroom.draw_area_light(
            points[0],
            points[1],
            self.light_length,
            float(self.light_dir),
        )
