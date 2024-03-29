import pygame
import SakuyaEngine as engine

KEYBOARD = {
    "up1": pygame.K_w,
    "left1": pygame.K_a,
    "down1": pygame.K_s,
    "right1": pygame.K_d,
    "up2": pygame.K_w,
    "left2": pygame.K_a,
    "down2": pygame.K_s,
    "right2": pygame.K_d,
    "A": pygame.K_z,
    "B": pygame.K_x,
    "X": None,
    "Y": None,
    "select": pygame.K_q,
    "start": pygame.K_ESCAPE,
}

MAX_FLOOR_BREAK_VAL = 25000

RANDOM_NOISE = pygame.image.load(
    engine.resource_path("data/sprites/random_noise.png")
).convert_alpha()
RANDOM_NOISE.set_alpha(5)
RANDOM_NOISE_SIZE = RANDOM_NOISE.get_size()
FLOOR_BREAK_TEXTURE = engine.split_image(
    pygame.image.load(
        engine.resource_path("data/sprites/breaking_animation.png")
    ).convert_alpha(),
    8,
    8,
)

TEXTBOOK_SPRITE = pygame.image.load(
    engine.resource_path("data/sprites/textbook.png")
).convert_alpha()

BACKGROUND_SPRITE = pygame.image.load(
    engine.resource_path("data/sprites/title_bg.png")
).convert_alpha()
