import argparse
import time
import pygame
import pypresence
import SakuyaEngine as engine
from data.scripts.const import _sounds, DISCORD_RPC_CLIENT_ID

client = engine.Client(
    "Stalker",
    pygame.Vector2(128, 112),
    mouse_image=pygame.image.load(engine.resource_path("data/sprites/mouse_pointer.png")),
    log_dir=".novial/stalker/logs",
)


def activate_rpc() -> None:
    try:
        rpc = pypresence.Presence(DISCORD_RPC_CLIENT_ID)
        rpc.connect()
        rpc.update(start=time.time())
    except:
        print("Something went wrong starting up Discord RPC.")


client.sounds = _sounds

from data.scenes.maintitle import MainTitle
from data.scenes.mainworld import MainWorld

client.scene_manager.register_scene(MainTitle)
client.scene_manager.register_scene(MainWorld)

parser = argparse.ArgumentParser()
parser.add_argument("--scene", type=str, help="Load a scene")
parser.add_argument("--fps", type=int, help="Set the game fps")
parser.add_argument(
    "--rpc", type=bool, help="Enables/disables Discord RPC; enabled on default"
)
args = parser.parse_args()

client.max_fps = 60

if args.fps is not None:
    client.max_fps = args.fps

if args.scene is not None:
    client.add_scene(args.scene)
else:
    client.add_scene("MainWorld")

if args.rpc is None or args.rpc:
    activate_rpc()

client.main()
