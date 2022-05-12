from data.scripts.const import RANDOM_NOISE, RANDOM_NOISE_SIZE

import random
import SakuyaEngine as engine


def apply_noise(scene: engine.Scene):
    rand_pos = random.randint(-int(RANDOM_NOISE_SIZE[0] / 3), 0), random.randint(
        -int(RANDOM_NOISE_SIZE[1] / 3), 0
    )
    scene.screen.blit(RANDOM_NOISE, (rand_pos))
