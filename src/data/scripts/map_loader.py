import pytmx
import pygame


class GameMap:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.data = pytmx.TiledMap(file_path)
        self.collision_rects = []
        self.light_col_rects = []
        self.interact_objs = []
        self.stalkerai_floor_objs = []

        self.surface = pygame.Surface(
            (
                self.data.width * self.data.tilewidth,
                self.data.height * self.data.tileheight,
            )
        )

        for layer in self.data.visible_tile_layers:
            layer = self.data.layers[layer]
            for x, y, image in layer.tiles():
                dim = image[1]
                img = pygame.image.load(image[0]).convert_alpha()
                cropped_img = img.subsurface(dim)
                self.surface.blit(
                    cropped_img, (x * self.data.tilewidth, y * self.data.tileheight)
                )

        for obj in self.data.objects:
            if obj.type and obj.visible:
                if obj.type == "collision_rect":
                    col_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    self.collision_rects.append(col_rect)

                    if obj.properties["light_col"]:
                        light_rect = pygame.Rect(
                            obj.x, obj.y, obj.width - 1, obj.height - 1
                        )
                        self.light_col_rects.append(light_rect)

                elif obj.type == "interact":
                    r = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    self.interact_objs.append(
                        {
                            "rect": r,
                            "hint": obj.properties["hint"],
                            "cmd": obj.properties["cmd"],
                        }
                    )

                elif obj.type == "stalker_floor_rect":
                    rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    self.stalkerai_floor_objs.append(rect)

    @property
    def size(self) -> pygame.Vector2:
        return pygame.Vector2(
            self.data.width * self.data.tilewidth,
            self.data.height * self.data.tileheight,
        )
