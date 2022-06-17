import argparse
import time
import logging
import sys
import pygame
import pypresence
import SakuyaEngine as engine
from data.scripts.const import _sounds, DISCORD_RPC_CLIENT_ID

if __name__ != "__main__":
    sys.exit()

client = engine.Client(
    "Stalker",
    pygame.Vector2(128, 112),
    mouse_image=pygame.image.load(
        engine.resource_path("data/sprites/mouse_pointer.png")
    ),
    log_dir=".novial/stalker/logs",
)


def activate_rpc() -> None:
    try:
        rpc = pypresence.Presence(DISCORD_RPC_CLIENT_ID)
        rpc.connect()
        rpc.update(start=time.time())
    except (
        ConnectionRefusedError,
        pypresence.exceptions.DiscordNotFound,
        pypresence.exceptions.DiscordError,
    ):
        logging.error("Something went wrong starting up Discord RPC.")


client.sounds = _sounds

from data.scenes.maintitle import MainTitle
from data.scenes.mainworld import MainWorld

client.scene_manager.register_scene(MainTitle)
client.scene_manager.register_scene(MainWorld)

parser = argparse.ArgumentParser()
parser.add_argument("--scene", type=str, help="Load a scene", default="MainTitle")
parser.add_argument("--fps", type=int, help="Set the game fps", default=60)
parser.add_argument(
    "--no-rpc", help="Disables Discord RPC", action=argparse.BooleanOptionalAction
)
args = parser.parse_args()

if args.fps:
    client.max_fps = args.fps

if args.scene:
    client.add_scene(args.scene)

if args.no_rpc is None:
    logging.info("Activating Discord RPC")
    activate_rpc()

client.main()
