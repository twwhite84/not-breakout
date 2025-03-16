from IState import IState

class MainMenuState(IState):
    def __init__(self, window, renderer) -> None:
        pass

    def update(self, et: float) -> None:
        pass

    def render(self) -> None:
        pass

    def onEnter(self) -> bool:
        print("MAIN MENU STATE -- ENTRY")
        return True
    
    def onExit(self) -> bool:
        print("MAIN MENU STATE -- EXIT")
        return False