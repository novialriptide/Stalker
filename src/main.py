import argparse
import pygame
import SakuyaEngine as engine

client = engine.Client(
    f"Stay Alert",
    pygame.Vector2(128, 112),
    mouse_image=pygame.image.load("data/sprites/mouse_pointer.png"),
)

pygame.mixer.init()
pygame.mixer.set_num_channels(64)

from data.scenes.maintitle import MainTitle
from data.scenes.mainworld import MainWorld

scenes = [MainTitle, MainWorld]
scene_manager = engine.SceneManager(client)
for s in scenes:
    scene_manager.register_scene(s)

parser = argparse.ArgumentParser()
parser.add_argument("--scene", type=str, help="Load a scene")
parser.add_argument("--fps", type=int, help="Set the game fps")
args = parser.parse_args()

client.max_fps = 60

if args.fps is not None:
    client.max_fps = args.fps

if args.scene is not None:
    client.add_scene(args.scene)
else:
    client.add_scene("MainWorld")

client.main()
