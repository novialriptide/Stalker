import SakuyaEngine as engine
import pygame

DISCORD_RPC_CLIENT_ID = 979044467703181322
HOMEWORK_QUOTA = 20000
PX_INTERACT_MIN_DISTANCE = 15

pygame.mixer.init()

_sounds = {
    "open_window": engine.Sound(
        engine.resource_path("data/audio/game_window_open.mp3")
    ),
    "close_window": engine.Sound(
        engine.resource_path("data/audio/game_window_close.mp3")
    ),
    "homework_progress": engine.Sound(
        engine.resource_path("data/audio/game_homework_pencil.mp3"), cooldown=1700
    ),
    "white_noise": engine.Sound(
        engine.resource_path("data/audio/game_whitenoise.wav"), volume=0.2
    ),
    "footstep1": engine.Sound(
        engine.resource_path("data/audio/game_footstep1.mp3"), cooldown=500
    ),
    "floor_bang": engine.Sound(
        engine.resource_path("data/audio/game_floor_bang.mp3"), cooldown=1500
    ),
    "textbook_slam": engine.Sound(
        engine.resource_path("data/audio/game_textbook_slam.mp3")
    ),
    "flashlight_on": engine.Sound(
        engine.resource_path("data/audio/game_flashlight_on.wav")
    ),
}
