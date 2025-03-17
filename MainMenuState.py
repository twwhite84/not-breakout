from IState import IState
import sdl2
from sdl2 import sdlttf
from typing import cast
import ctypes
import Colors


class MainMenuState(IState):
    def __init__(self, window: sdl2.SDL_Window, renderer: sdl2.SDL_Renderer) -> None:
        self.window = window
        self.screen_width_c: ctypes.c_int = ctypes.c_int(0)
        self.screen_height_c: ctypes.c_int = ctypes.c_int(0)
        sdl2.SDL_GetWindowSize(
            window,
            ctypes.pointer(self.screen_width_c),
            ctypes.pointer(self.screen_height_c),
        )
        self.screen_width = self.screen_width_c.value
        self.screen_height = self.screen_height_c.value
        self.renderer = renderer

        font_bitwise = sdlttf.TTF_OpenFont(b"fonts/8bitOperatorPlus-Bold.ttf", 32)
        text_surface_a: sdl2.SDL_Surface = sdlttf.TTF_RenderText_Solid(
            font_bitwise, b"Not Breakout", sdl2.SDL_Color(*Colors.YELLOW)
        )
        sdlttf.TTF_CloseFont(font_bitwise)
        self.text_texture_a = sdl2.SDL_CreateTextureFromSurface(
            renderer, text_surface_a
        )

    def update(self, et: int) -> None:
        pass

    def render(self) -> None:

        srcWidth_c: ctypes.c_int = ctypes.c_int(0)
        srcHeight_c: ctypes.c_int = ctypes.c_int(0)
        _ = sdl2.SDL_QueryTexture(
            self.text_texture_a, None, None, srcWidth_c, srcHeight_c
        )
        srcWidth: int = srcWidth_c.value
        srcHeight: int = srcHeight_c.value

        pasteArea: sdl2.SDL_Rect = sdl2.SDL_Rect(
            int(0.5 * self.screen_width - 0.5 * srcWidth * 3),
            int(0.25 * self.screen_height - 0.5 * srcHeight * 3),
            int(srcWidth * 3),
            int(srcHeight * 3),
        )
        sdl2.SDL_RenderCopy(self.renderer, self.text_texture_a, None, pasteArea)

    def onEnter(self) -> bool:
        print("MAIN MENU STATE -- ENTRY")
        return True

    def onExit(self) -> bool:
        print("MAIN MENU STATE -- EXIT")
        return True
