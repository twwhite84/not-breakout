from GameObject import GameObject
import sdl2


class Player(GameObject):

    def __init__(self, x, y, w, h, color: tuple):
        super().__init__(x, y, w, h, color)
        self.speed = 500

    def render(self, renderer: sdl2.SDL_Renderer) -> None:
        super().render(renderer)
