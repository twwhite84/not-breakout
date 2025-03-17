from IState import IState
import sdl2
from sdl2 import sdlttf
import ctypes
import Colors
import math
from StateMachine import StateMachine, StateCode


class IntroState(IState):
    def __init__(
        self, window: sdl2.SDL_Window, renderer: sdl2.SDL_Renderer, fsm: StateMachine
    ) -> None:
        self.window = window
        self.screen_width_c: ctypes.c_int = ctypes.c_int(0)
        self.screen_height_c: ctypes.c_int = ctypes.c_int(0)
        sdl2.SDL_GetWindowSize(
            window,
            ctypes.pointer(self.screen_width_c),
            ctypes.pointer(self.screen_height_c),
        )
        self.screen_width: int = self.screen_width_c.value
        self.screen_height: int = self.screen_height_c.value
        self.renderer = renderer
        self.fsm = fsm

        font_joystix = sdlttf.TTF_OpenFont(b"fonts\joystix_mono.otf", 24)

        def makeText(text: bytes, color: tuple[int, int, int, int]) -> sdl2.SDL_Texture:
            text_surface: sdl2.SDL_Surface = sdlttf.TTF_RenderText_Solid(
                font_joystix, text, sdl2.SDL_Color(*color)
            )
            return sdl2.SDL_CreateTextureFromSurface(renderer, text_surface)

        self.text_texture_title_odd_bg = makeText(b"N t B e k u ", Colors.RED)
        self.text_texture_title_odd_fg = makeText(b"N t B e k u ", Colors.YELLOW)
        self.text_texture_title_even_bg = makeText(b" o   r a o t", Colors.RED)
        self.text_texture_title_even_fg = makeText(b" o   r a o t", Colors.YELLOW)
        self.text_texture_playgame = makeText(b"PRESS ENTER TO START", Colors.WHITE)

        sdlttf.TTF_CloseFont(font_joystix)

        self.yoffset_odd: int = 0
        self.rotang: float = 0

    def processEvents(self, event: sdl2.SDL_Event) -> bool:
        while sdl2.SDL_PollEvent(ctypes.byref(event)):
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    quitEvent = sdl2.SDL_Event()
                    quitEvent.type = sdl2.SDL_QUIT
                    sdl2.SDL_PushEvent(ctypes.byref(quitEvent))

                elif event.key.keysym.sym == sdl2.SDLK_RETURN:
                    self.fsm.changeState(StateCode.PLAY)

            if event.type == sdl2.SDL_QUIT:
                return True

        return False

    def update(self, et: int) -> None:
        self.rotang += 0.0015 * et
        self.yoffset_odd = int(math.sin(self.rotang * math.pi) * 20)
        self.yoffset_even = int(math.sin(self.rotang * math.pi - (0.25 * math.pi)) * 20)

        sdl2.SDL_SetTextureColorMod(
            self.text_texture_playgame,
            abs(int(math.sin(self.rotang * math.pi) * 255)),
            abs(int(math.sin(self.rotang * math.pi - (0.25 * math.pi)) * 255)),
            abs(int(math.sin(self.rotang * math.pi - (0.75 * math.pi)) * 255)),
        )

    def render(self) -> None:

        srcWidth_c: ctypes.c_int = ctypes.c_int(0)
        srcHeight_c: ctypes.c_int = ctypes.c_int(0)

        # title text
        sdl2.SDL_QueryTexture(
            self.text_texture_title_odd_bg, None, None, srcWidth_c, srcHeight_c
        )
        title_w: int = srcWidth_c.value
        title_h: int = srcHeight_c.value

        def renderTitle(text: sdl2.SDL_Texture, y_offset: int, shadow: int = 0) -> None:
            pasteArea: sdl2.SDL_Rect = sdl2.SDL_Rect(
                int(0.5 * self.screen_width - 0.5 * title_w * 3) + shadow,
                int(0.33 * self.screen_height - 0.5 * title_h * 3 + y_offset) + shadow,
                int(title_w * 3),
                int(title_h * 3),
            )
            sdl2.SDL_RenderCopy(self.renderer, text, None, pasteArea)

        renderTitle(self.text_texture_title_odd_bg, self.yoffset_odd)
        renderTitle(self.text_texture_title_even_bg, self.yoffset_even)
        renderTitle(self.text_texture_title_odd_fg, self.yoffset_odd, shadow=5)
        renderTitle(self.text_texture_title_even_fg, self.yoffset_even, shadow=5)

        # press play text
        sdl2.SDL_QueryTexture(
            self.text_texture_playgame, None, None, srcWidth_c, srcHeight_c
        )
        text_play_w: int = srcWidth_c.value
        text_play_h: int = srcHeight_c.value
        pasteArea = sdl2.SDL_Rect(
            int(0.5 * self.screen_width - 0.5 * text_play_w * 1.25),
            int(0.75 * self.screen_height - 0.5 * text_play_h * 1.25),
            int(text_play_w * 1.25),
            int(text_play_h * 1.25),
        )
        sdl2.SDL_RenderCopy(self.renderer, self.text_texture_playgame, None, pasteArea)

    def onEnter(self) -> bool:
        print("INTRO STATE -- ENTRY")
        return True

    def onExit(self) -> bool:
        print("INTRO STATE -- EXIT")
        return True
