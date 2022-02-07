import argparse
import pygame

from SakuyaEngine.client import Client
from SakuyaEngine.scene import SceneManager

client = Client(
    f"Stay Alert",
    pygame.Vector2(256 * 1.5, 224 * 1.5),
)

pygame.mixer.init()
pygame.mixer.set_num_channels(64)

from data.scenes.maintitle import MainTitle
from data.scenes.mainworld import MainWorld

scenes = [
    MainTitle,
    MainWorld
]
scene_manager = SceneManager(client)
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