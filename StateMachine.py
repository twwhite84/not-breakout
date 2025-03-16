# This is based on code shown in book SDL Game Development by Shaun Mitchell

from IState import IState

class StateMachine():
    def __init__(self) -> None:
        self.state_list: list[IState] = []

    def changeState(self, state: IState) -> None:
        if len(self.state_list) > 0:
            if id(self.state_list[-1]) == id(state):
                return
            if self.state_list[-1].onExit():
                self.state_list.pop()

        self.state_list.append(state)
        self.state_list[-1].onEnter()

    def pushState(self, state: IState) -> None:
        self.state_list.append(state)
        self.state_list[-1].onEnter()

    def popState(self) -> None:
        if len(self.state_list) > 0:
            if self.state_list[-1].onExit():
                self.state_list.pop()

    def update(self, et: float) -> None:
        if len(self.state_list) > 0:
           self.state_list[-1].update(et)

    def render(self):
        if len(self.state_list) > 0:
            self.state_list[-1].render() 