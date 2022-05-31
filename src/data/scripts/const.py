import SakuyaEngine as engine
import pygame

DISCORD_RPC_CLIENT_ID = 979044467703181322
HOMEWORK_QUOTA = 20000
PX_INTERACT_MIN_DISTANCE = 15

pygame.mixer.init()

_sounds = {
    "open_window": engine.Sound("data/audio/game_window_open.mp3"),
    "close_window": engine.Sound("data/audio/game_window_close.mp3"),
    "homework_progress": engine.Sound(
        "data/audio/game_homework_pencil.mp3", cooldown=1700
    ),
    "white_noise": engine.Sound("data/audio/game_whitenoise.wav"),
    "footstep1": engine.Sound("data/audio/game_footstep1.mp3", cooldown=500),
}
