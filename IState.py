from abc import ABCMeta, abstractmethod
import sdl2

# from StateMachine import StateMachine


class IState(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, window: sdl2.SDL_Window, renderer: sdl2.SDL_Renderer) -> None:
        pass

    @abstractmethod
    def update(self, et: int) -> None:
        pass

    @abstractmethod
    def render(self) -> None:
        pass

    @abstractmethod
    def onEnter(self) -> bool:
        pass

    @abstractmethod
    def onExit(self) -> bool:
        pass
