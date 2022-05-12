def close_window(**kwargs) -> None:
    window = kwargs["window"]
    window.open_percent = 0


def do_homework(**kwargs) -> None:
    scene = kwargs["scene"]
    scene.doing_homework = True


CMDS = {"close_win": close_window, "do_homework": do_homework}
