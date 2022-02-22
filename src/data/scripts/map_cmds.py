import pygame


def hide(**kwargs) -> None:
    player = kwargs["player"]
    rect = kwargs["rect"]
    
    if player.hide_cooldown_val <= player.hide_cooldown_clock.get_time():
        player.hide_cooldown_clock.reset()
        player_rect = player.rect
        player.target_position = pygame.Vector2(
            rect.x + rect.width / 2 - player_rect.width / 2,
            rect.y + rect.height / 2 - player_rect.height / 2,
        )
        player.back_hide_pos = player.position
        player.hiding = True


CMDS = {"hide": hide}
