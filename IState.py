from abc import ABCMeta, abstractmethod

class IState(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, window, renderer) -> None:
        pass
    
    @abstractmethod
    def update(self, et: float) -> None:
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