from GameObject import GameObject
import sdl2
from Vector import Vector


class Ball(GameObject):

    def __init__(
        self, x: int, y: int, w: int, h: int, color: tuple[int, int, int, int]
    ):
        super().__init__(x, y, w, h, color)
        self.speed: float = 0.3
        self.direction: Vector = Vector(0, 1)

    def render(self, renderer: sdl2.SDL_Renderer) -> None:
        super().render(renderer)
