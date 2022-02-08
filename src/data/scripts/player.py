from .entity import Entity

class Player(Entity):
    def on_update(self) -> None:
        print("d")