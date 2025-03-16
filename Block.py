from GameObject import GameObject
import sdl2


class Block(GameObject):

    def __init__(
        self, x: int, y: int, w: int, h: int, color: tuple[int, int, int, int]
    ):
        super().__init__(x, y, w, h, color)

    def render(self, renderer: sdl2.SDL_Renderer) -> None:
        super().render(renderer)
