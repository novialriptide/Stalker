from SakuyaEngine.tile import crop_tile_image

import pytmx
import pygame


class GameMap:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.data = pytmx.TiledMap(file_path)
        self.collision_rects = []
        self.light_col_rects = []
        self.interact_rects = []

        self.surface = pygame.Surface(
            (
                self.data.width * self.data.tilewidth,
                self.data.height * self.data.tileheight,
            )
        )

        for layer in self.data.visible_tile_layers:
            layer = self.data.layers[layer]
            for (
                x,
                y,
                image,
            ) in layer.tiles():
                dim = image[1]
                img = pygame.image.load(image[0]).convert_alpha()
                cropped_img = img.subsurface(dim)
                self.surface.blit(
                    cropped_img, (x * self.data.tilewidth, y * self.data.tileheight)
                )

        for obj in self.data.objects:
            if obj.type:
                if obj.type == "collision_rect":
                    r = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    self.collision_rects.append(r)

                elif obj.type == "light_col_rect":
                    r = pygame.Rect(obj.x, obj.y, obj.width - 1, obj.height - 1)
                    self.light_col_rects.append(r)
                
                elif obj.type == "interact":
                    r = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    self.interact_rects.append(r)

    @property
    def size(self) -> pygame.Vector2:
        return pygame.Vector2(
            self.data.width * self.data.tilewidth,
            self.data.height * self.data.tileheight,
        )
