from IState import IState
import sdl2


class MainMenuState(IState):
    def __init__(self, window: sdl2.SDL_Window, renderer: sdl2.SDL_Renderer) -> None:
        pass

    def update(self, et: int) -> None:
        pass

    def render(self) -> None:
        pass

    def onEnter(self) -> bool:
        print("MAIN MENU STATE -- ENTRY")
        return True

    def onExit(self) -> bool:
        print("MAIN MENU STATE -- EXIT")
        return False
