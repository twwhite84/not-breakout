from IRenderable import IRenderable
import sdl2


class GameObject(IRenderable):
    def __init__(
        self, x: int, y: int, w: int, h: int, color: tuple[int, int, int, int]
    ) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        self._y = value

    def render(self, renderer: sdl2.SDL_Renderer) -> None:
        renderable = sdl2.SDL_Rect(
            int(self.x - 0.5 * self.w),
            int(self.y - 0.5 * self.h),
            int(self.w),
            int(self.h),
        )
        sdl2.SDL_SetRenderDrawColor(renderer, *self.color)
        sdl2.SDL_RenderFillRect(renderer, renderable)
