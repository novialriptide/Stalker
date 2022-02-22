class Window:
    def __init__(
        self,
        rect,
        light_length,
        light_dir,
        window_dir,
    ) -> None:
        self.rect = rect
        self.light_length = light_length
        self.light_dir = light_dir
        self.window_dir = window_dir

    @property
    def area_light_points(self):
        return None
