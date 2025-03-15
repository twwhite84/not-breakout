from abc import ABCMeta, abstractmethod
import sdl2


class IRenderable(metaclass=ABCMeta):
    @abstractmethod
    def render(self, renderer: sdl2.SDL_Renderer) -> None:
        pass
