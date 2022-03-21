import pygame

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

RANDOM_NOISE = pygame.image.load("data/sprites/random_noise.png").convert_alpha()
RANDOM_NOISE.set_alpha(10)
RANDOM_NOISE_SIZE = RANDOM_NOISE.get_size()

OPEN_WINDOW_SOUND = pygame.mixer.Sound("data/audio/game_window_open.mp3")
CLOSE_WINDOW_SOUND = pygame.mixer.Sound("data/audio/game_window_close.mp3")
