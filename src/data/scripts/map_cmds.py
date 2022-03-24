import pygame

def close_window(**kwargs) -> None:
    window = kwargs["window"]
    window.open_percent = 0


CMDS = {"close_win": close_window}
