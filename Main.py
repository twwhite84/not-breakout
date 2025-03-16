import sys
import ctypes
import sdl2
import Colors
from StateMachine import StateMachine
from PlayState import PlayState


class Main:
    def __init__(self) -> None:
        self.SCREEN_WIDTH: int = 800
        self.SCREEN_HEIGHT: int = 600

        sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
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
        self.fsm.pushState(PlayState(self.window, self.renderer))
        self.event = sdl2.SDL_Event()
        self.running = True

    def processEvents(self) -> None:
        while sdl2.SDL_PollEvent(ctypes.byref(self.event)):
            if self.event.type == sdl2.SDL_QUIT:
                self.running = False
                break

    def update(self, et: float) -> None:
        self.fsm.update(et)

    def render(self) -> None:
        sdl2.SDL_SetRenderDrawColor(self.renderer, *Colors.BLACK)
        sdl2.SDL_RenderClear(self.renderer)
        self.fsm.render()
        sdl2.SDL_RenderPresent(self.renderer)

    def run(self) -> None:
        MAX_FPS = 60
        TARGET_SPF = 1 / MAX_FPS
        dt = sdl2.SDL_GetTicks()

        self.running = True
        while self.running:
            prev_dt = dt
            dt = sdl2.SDL_GetTicks()
            et = (dt - prev_dt) / 1000.0
            if et < TARGET_SPF:
                sdl2.SDL_Delay(int((TARGET_SPF - et) * 1000))

            self.processEvents()
            self.update(float(et))
            self.render()

        # shutdown
        sdl2.SDL_DestroyRenderer(self.renderer)
        sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()


main = Main()
main.run()
