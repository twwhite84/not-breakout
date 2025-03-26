from GameObject import GameObject
import sdl2


class Player(GameObject):

    def __init__(
        self, x: int, y: int, w: int, h: int, color: tuple[int, int, int, int]
    ):
        super().__init__(x, y, w, h, color)
        self.speed: float = 0.25

    def render(self, renderer: sdl2.SDL_Renderer) -> None:
        super().render(renderer)
