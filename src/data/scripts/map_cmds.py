import pygame


def hide(**kwargs) -> None:
    player = kwargs["player"]
    rect = kwargs["rect"]
    
    if player.hide_cooldown_val <= player.hide_cooldown_clock.get_time():
        player_rect = player.rect
        player.target_position = pygame.Vector2(
            rect.x + rect.width / 2 - player_rect.width / 2,
            rect.y + rect.height / 2 - player_rect.height / 2,
        )
        player.back_hide_pos = player.position
        player.hiding = True

def close_window(**kwargs) -> None:
    window = kwargs["window"]
    window.open_percent = 0

CMDS = {"hide": hide, "close_win": close_window}
