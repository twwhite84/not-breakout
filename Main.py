import sys
import sdl2
from sdl2 import sdlttf
import Colors
from StateMachine import StateMachine, StateCode
from PlayState import PlayState
from IntroState import IntroState
from typing import cast


class Main:
    def __init__(self) -> None:
        self.SCREEN_WIDTH: int = 800
        self.SCREEN_HEIGHT: int = 600

        sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
        sdlttf.TTF_Init()

        self.window = sdl2.SDL_CreateWindow(
            b"Not Breakout",
            sdl2.SDL_WINDOWPOS_CENTERED,
            sdl2.SDL_WINDOWPOS_CENTERED,
            self.SCREEN_WIDTH,
            self.SCREEN_HEIGHT,
            sdl2.SDL_WINDOW_SHOWN,
        )
        self.renderer = sdl2.SDL_CreateRenderer(
            self.window, -1, sdl2.SDL_RENDERER_SOFTWARE
        )

        self.fsm = StateMachine()
        self.fsm.addState(
            StateCode.INTRO, IntroState(self.window, self.renderer, self.fsm)
        )
        self.fsm.addState(
            StateCode.PLAY, PlayState(self.window, self.renderer, self.fsm)
        )
        self.fsm.changeState(StateCode.INTRO)

        self.event = sdl2.SDL_Event()
        self.running = True

    def processEvents(self, event: sdl2.SDL_Event) -> None:
        if self.fsm.processEvents(event):
            self.running = False

    def update(self, et: int) -> None:
        self.fsm.update(et)

    def render(self) -> None:
        sdl2.SDL_SetRenderDrawColor(self.renderer, *Colors.BLACK)
        sdl2.SDL_RenderClear(self.renderer)
        self.fsm.render()
        sdl2.SDL_RenderPresent(self.renderer)

    def run(self) -> None:
        MAX_FPS: int = 60
        TARGET_MSPF: int = int((1 / MAX_FPS) * 1000)
        dt: int = 0

        self.running = True
        while self.running:
            prev_dt: int = dt
            dt = cast(int, sdl2.SDL_GetTicks())
            et: int = dt - prev_dt
            if et < TARGET_MSPF:
                sdl2.SDL_Delay(TARGET_MSPF - et)

            self.processEvents(self.event)
            self.update(et)
            self.render()

        # shutdown
        sdlttf.TTF_Quit()
        sdl2.SDL_DestroyRenderer(self.renderer)
        sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()


main = Main()
main.run()
