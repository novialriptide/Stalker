from SakuyaEngine.tile import crop_tile_image

import pytmx
import pygame

class GameMap:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.tiled_map = pytmx.TiledMap(file_path)
        
        self.surface = pygame.Surface((self.tiled_map.width * self.tiled_map.tilewidth, self.tiled_map.height * self.tiled_map.tileheight))
        
        for layer in self.tiled_map.visible_tile_layers:
            layer = self.tiled_map.layers[layer]
            for x, y, image, in layer.tiles():
                dim = image[1]
                img = pygame.image.load(image[0]).convert_alpha()
                cropped_img = crop_tile_image(img, dim[0], dim[1], dim[2], dim[3])
                self.surface.blit(cropped_img, (x * self.tiled_map.tilewidth, y * self.tiled_map.tileheight))
        
        for obj in self.tiled_map.objects:
            print(obj)