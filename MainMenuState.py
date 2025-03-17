from IState import IState
import sdl2
from sdl2 import sdlttf
from typing import cast
import ctypes
import Colors
import math


class MainMenuState(IState):
    def __init__(self, window: sdl2.SDL_Window, renderer: sdl2.SDL_Renderer) -> None:
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

        font_bitwise = sdlttf.TTF_OpenFont(b"fonts\joystix_mono.otf", 24)

        # title text -- odd letters bg
        text_surface: sdl2.SDL_Surface = sdlttf.TTF_RenderText_Solid(
            font_bitwise, b"N t B e k u ", sdl2.SDL_Color(*Colors.RED)
        )
        self.text_texture_title_odd_bg = sdl2.SDL_CreateTextureFromSurface(
            renderer, text_surface
        )

        # title text -- odd letters fg
        text_surface = sdlttf.TTF_RenderText_Solid(
            font_bitwise, b"N t B e k u ", sdl2.SDL_Color(*Colors.YELLOW)
        )
        self.text_texture_title_odd_fg = sdl2.SDL_CreateTextureFromSurface(
            renderer, text_surface
        )

        # title text -- even letters bg
        text_surface = sdlttf.TTF_RenderText_Solid(
            font_bitwise, b" o   r a o t", sdl2.SDL_Color(*Colors.RED)
        )
        self.text_texture_title_even_bg = sdl2.SDL_CreateTextureFromSurface(
            renderer, text_surface
        )

        # title text -- even letters fg
        text_surface = sdlttf.TTF_RenderText_Solid(
            font_bitwise, b" o   r a o t", sdl2.SDL_Color(*Colors.YELLOW)
        )
        self.text_texture_title_even_fg = sdl2.SDL_CreateTextureFromSurface(
            renderer, text_surface
        )

        # play text
        text_surface = sdlttf.TTF_RenderText_Solid(
            font_bitwise, b"PRESS ENTER TO START", sdl2.SDL_Color(*Colors.WHITE)
        )
        self.text_texture_playgame = sdl2.SDL_CreateTextureFromSurface(
            renderer, text_surface
        )

        sdlttf.TTF_CloseFont(font_bitwise)

        self.yoffset_odd: int = 0
        self.mystep: float = 0

    def update(self, et: int) -> None:
        self.mystep += 0.0015 * et
        self.yoffset_odd = int(math.sin(self.mystep * math.pi) * 20)
        self.yoffset_even = int(math.sin(self.mystep * math.pi - (0.25 * math.pi)) * 20)

        sdl2.SDL_SetTextureColorMod(
            self.text_texture_playgame,
            abs(int(math.sin(self.mystep * math.pi) * 255)),
            abs(int(math.sin(self.mystep * math.pi - (0.25 * math.pi)) * 255)),
            abs(int(math.sin(self.mystep * math.pi - (0.75 * math.pi)) * 255)),
        )

    def render(self) -> None:

        srcWidth_c: ctypes.c_int = ctypes.c_int(0)
        srcHeight_c: ctypes.c_int = ctypes.c_int(0)
        _ = sdl2.SDL_QueryTexture(
            self.text_texture_title_odd_bg, None, None, srcWidth_c, srcHeight_c
        )
        srcWidth: int = srcWidth_c.value
        srcHeight: int = srcHeight_c.value

        # title odd bg
        pasteArea: sdl2.SDL_Rect = sdl2.SDL_Rect(
            int(0.5 * self.screen_width - 0.5 * srcWidth * 3),
            int(0.33 * self.screen_height - 0.5 * srcHeight * 3 + self.yoffset_odd),
            int(srcWidth * 3),
            int(srcHeight * 3),
        )
        sdl2.SDL_RenderCopy(
            self.renderer, self.text_texture_title_odd_bg, None, pasteArea
        )

        # title even bg
        pasteArea = sdl2.SDL_Rect(
            int(0.5 * self.screen_width - 0.5 * srcWidth * 3),
            int(0.33 * self.screen_height - 0.5 * srcHeight * 3 + self.yoffset_even),
            int(srcWidth * 3),
            int(srcHeight * 3),
        )
        sdl2.SDL_RenderCopy(
            self.renderer, self.text_texture_title_even_bg, None, pasteArea
        )

        # title odd fg
        pasteArea = sdl2.SDL_Rect(
            int(0.5 * self.screen_width - 0.5 * srcWidth * 3) + 5,
            int(0.33 * self.screen_height - 0.5 * srcHeight * 3 + self.yoffset_odd) + 5,
            int(srcWidth * 3),
            int(srcHeight * 3),
        )
        sdl2.SDL_RenderCopy(
            self.renderer, self.text_texture_title_odd_fg, None, pasteArea
        )

        # title even fg
        pasteArea = sdl2.SDL_Rect(
            int(0.5 * self.screen_width - 0.5 * srcWidth * 3) + 5,
            int(0.33 * self.screen_height - 0.5 * srcHeight * 3 + self.yoffset_even)
            + 5,
            int(srcWidth * 3),
            int(srcHeight * 3),
        )
        sdl2.SDL_RenderCopy(
            self.renderer, self.text_texture_title_even_fg, None, pasteArea
        )

        pasteArea = sdl2.SDL_Rect(
            int(0.5 * self.screen_width - 0.5 * srcWidth * 2),
            int(0.75 * self.screen_height - 0.5 * srcHeight * 2),
            int(srcWidth * 2),
            int(srcHeight * 2),
        )
        sdl2.SDL_RenderCopy(self.renderer, self.text_texture_playgame, None, pasteArea)

    def onEnter(self) -> bool:
        print("MAIN MENU STATE -- ENTRY")
        return True

    def onExit(self) -> bool:
        print("MAIN MENU STATE -- EXIT")
        return True
