import pygame

def hide(**kwargs) -> None:
    rect = kwargs["rect"]
    player_rect = kwargs["player"].rect
    kwargs["player"].target_position = pygame.Vector2(
        rect.x + rect.width / 2 - player_rect.width / 2,
        rect.y + rect.height / 2 - player_rect.height / 2
    )
    kwargs["player"].back_hide_pos = kwargs["player"].position
    kwargs["player"].hiding = True

CMDS = {
    "hide": hide
}