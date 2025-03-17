from IState import IState
from enum import Enum
import sdl2


class StateCode(Enum):
    INTRO = 1
    PLAY = 2


class State:
    def __init__(self, state: IState, active: bool = False) -> None:
        self.state: IState = state
        self.active: bool = active


class StateMachine:
    def __init__(self) -> None:
        self.state_map: dict[StateCode, State] = {}

    def changeState(self, code: StateCode) -> None:
        for key in self.state_map.keys():
            if self.state_map[key].active == True:
                self.state_map[key].active = False
                self.state_map[key].state.onExit()

        if code in self.state_map.keys():
            self.state_map[code].active = True
            self.state_map[code].state.onEnter()

    def addState(self, code: StateCode, state: IState) -> None:
        if code not in self.state_map.keys():
            self.state_map[code] = State(state)

    def dropState(self, code: StateCode) -> None:
        if code in self.state_map.keys():
            del self.state_map[code]

    def processEvents(self, event: sdl2.SDL_Event) -> bool:
        for code in self.state_map.keys():
            if self.state_map[code].active == True:
                if self.state_map[code].state.processEvents(event):
                    return True

        return False

    def update(self, et: int) -> None:
        for code in self.state_map.keys():
            state = self.state_map[code]
            if self.state_map[code].active == True:
                self.state_map[code].state.update(et)

    def render(self) -> None:
        for code in self.state_map.keys():
            if self.state_map[code].active == True:
                self.state_map[code].state.render()
