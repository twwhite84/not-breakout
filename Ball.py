from GameObject import GameObject
import sdl2
from Vector import Vector


class Ball(GameObject):

    def __init__(self, x, y, w, h, color: tuple):
        super().__init__(x, y, w, h, color)
        self.speed = 300
        self.direction = Vector(1, 1)

    def render(self, renderer: sdl2.SDL_Renderer) -> None:
        super().render(renderer)
