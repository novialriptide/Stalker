from typing import Tuple, Union
import SakuyaEngine as engine
import pygame
import random
import pytmx

def _random_rect_pos(rect: pygame.Rect) -> pygame.Vector2:
    return pygame.Vector2(
        random.randint(rect.x, rect.x + rect.width),
        random.randint(rect.y, rect.y + rect.height)
    )

def world_to_tile_pos(pos: pygame.Vector2, tiledmap: pytmx.TiledMap) -> pygame.Vector2:
    return pygame.Vector2(
        int(pos.x / tiledmap.tilewidth),
        int(pos.y / tiledmap.tileheight)
    )

class Floor:
    def __init__(self, pos: pygame.Vector2, pytmx_map: pytmx.TiledMap) -> None:
        self.pos = pos
        self.pytmx_map = pytmx_map
        self.world_pos = pygame.Vector2(
            pos.x * pytmx_map.tilewidth,
            pos.y * pytmx_map.tileheight
        )
        self.progress_clock = engine.Clock()

class FloorBreakManager:
    def __init__(self, stalkerai: "StalkerAI") -> None:
        self.stalkerai = stalkerai
        self.floors = []
        self.current_floor_index = None

    @property
    def current_floor(self) -> Union[Floor, None]:
        if self.current_floor_index is None:
            return None
        
        return self.floors[self.current_floor_index]

    def get_floor(self, pos: pygame.Vector2) -> Tuple[Floor, int]:
        for index, f in enumerate(self.floors):
            if f.pos == pos:
                return f, index
        return None, None

    def choose_floor(self) -> pygame.Vector2:
        scene = self.stalkerai.scene
        pytmx_map = scene.game_map.data
        stalkerai_rects = self.stalkerai.scene.game_map.stalkerai_floor_objs

        selected_rect = random.choice(stalkerai_rects)
        world_pos = _random_rect_pos(selected_rect)
        pos = world_to_tile_pos(world_pos, self.stalkerai.scene.game_map.data)

        self.floors.append(Floor(pos, pytmx_map))
        floor, index = self.get_floor(pos)
        self.current_floor_index = index
        
        self.current_floor.progress_clock.pause()

        self.current_floor_index = index
        floor.progress_clock.resume()

    def cancel_floor(self) -> None:
        self.current_floor.progress_clock.pause()
        self.current_floor_index = None
