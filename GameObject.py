from IRenderable import IRenderable
import sdl2


class GameObject(IRenderable):
    def __init__(self, x, y, w, h, color: tuple) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    @property
    def x(self):
        return int(self._x)

    @x.setter
    def x(self, value):
        self._x = int(value)

    @property
    def y(self):
        return int(self._y)

    @y.setter
    def y(self, value):
        self._y = int(value)

    def render(self, renderer: sdl2.SDL_Renderer) -> None:
        renderable = sdl2.SDL_Rect(
            int(self.x - 0.5 * self.w),
            int(self.y - 0.5 * self.h),
            int(self.w),
            int(self.h),
        )
        sdl2.SDL_SetRenderDrawColor(renderer, *self.color)
        sdl2.SDL_RenderFillRect(renderer, renderable)
