import sys
import ctypes
import sdl2
import Colors
from Player import Player
from Ball import Ball
from Block import Block
from IRenderable import IRenderable
from GameObject import GameObject
from typing import Iterable, List, Union, cast
from Hitside import Hitside
import math


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
        self.event = sdl2.SDL_Event()
        self.blocks: Iterable[Block] = self.makeBlocks()
        self.running = True

        # player
        width = 100
        height = 20
        self.player: Player = Player(
            self.SCREEN_WIDTH * 0.5,
            self.SCREEN_HEIGHT - 50,
            width,
            height,
            Colors.WHITE,
        )

        # ball
        width = 20
        height = 20
        self.ball: Ball = Ball(
            self.SCREEN_WIDTH * 0.5,
            self.SCREEN_HEIGHT * 0.5 - height * 0.5,
            width,
            height,
            Colors.CYAN,
        )

        self.renderables: Iterable[Union[IRenderable | Iterable[IRenderable]]] = [
            self.blocks,
            self.player,
            self.ball,
        ]

    def makeBlocks(self) -> Iterable[Block]:
        blocks: List[Block] = []

        block_width = 50
        block_height = 25
        margin = 10
        x_offset = 0.5 * block_width + margin + 5
        y_offset = 0.5 * block_height + margin
        colors = [
            Colors.RED,
            Colors.GREEN,
            Colors.BLUE,
            Colors.MAGENTA,
            Colors.YELLOW,
        ]

        for column in range(13):
            for row in range(5):
                blocks.append(
                    Block(
                        x_offset + column * (block_width + margin),
                        y_offset + row * (block_height + margin),
                        block_width,
                        block_height,
                        colors[row],
                    )
                )

        return blocks

    def isCollision(self, a: GameObject, b: GameObject) -> bool:
        if (
            (a.x < (b.x + 0.5 * b.w + 0.5 * a.w))
            and (a.x > (b.x - 0.5 * b.w - 0.5 * a.w))
            and (a.y < (b.y + 0.5 * b.h + 0.5 * a.h))
            and (a.y > (b.y - 0.5 * b.h - 0.5 * a.h))
        ):
            return True
        else:
            return False

    def findHitside(self, ball: Ball, obstacle: GameObject) -> Hitside:
        dy = ball.y - obstacle.y
        dx = ball.x - obstacle.x
        ang_side_portion = math.atan2(obstacle.h, obstacle.w)
        ang = math.atan2(dy, dx)

        if ang > (-math.pi + ang_side_portion) and ang <= (-ang_side_portion):
            return Hitside.top
        if ang > (ang_side_portion) and ang <= (math.pi - ang_side_portion):
            return Hitside.bottom
        if ang > (-ang_side_portion) and ang <= (ang_side_portion):
            return Hitside.right
        return Hitside.left

    def bounce(self, x: Ball, hitside: Hitside) -> None:
        # REMEMBER: down is positive in screen coords
        if hitside == Hitside.top:
            x.y -= 0.5 * x.h
            x.direction.y *= -1

        elif hitside == Hitside.bottom:
            x.y += 0.5 * x.h
            x.direction.y *= -1

        elif hitside == Hitside.right:
            x.x += 0.5 * x.w
            x.direction.x *= -1

        else:
            x.x -= 0.5 * x.w
            x.direction.x *= -1

    def processEvents(self) -> None:
        while sdl2.SDL_PollEvent(ctypes.byref(self.event)) != 0:
            if self.event.type == sdl2.SDL_Quit:
                self.running = False
                break

    def update(self, et) -> None:

        # handle keyboard input to move player, if within playfield
        currentKeyStates = sdl2.SDL_GetKeyboardState(None)
        if currentKeyStates[sdl2.SDL_SCANCODE_LEFT]:
            if not self.player.x - (0.5 * self.player.w) <= 0:
                self.player.x -= self.player.speed * et

        if currentKeyStates[sdl2.SDL_SCANCODE_RIGHT]:
            if not self.player.x + (0.5 * self.player.w) >= self.SCREEN_WIDTH:
                self.player.x += self.player.speed * et

        # ball collision -- wall
        if self.ball.x >= self.SCREEN_WIDTH:
            self.ball.direction.x *= -1
            self.ball.x -= self.ball.w * 0.5

        if self.ball.x <= 0:
            self.ball.direction.x *= -1
            self.ball.x += self.ball.w * 0.5

        if self.ball.y >= self.SCREEN_HEIGHT:
            # self.ball.direction.y *= -1
            # self.ball.y -= self.ball.h * 0.5

            # this should go to gameover state
            self.running = False

        if self.ball.y <= 0:
            self.ball.direction.y *= -1
            self.ball.y += self.ball.h * 0.5

        # ball collision -- player
        if self.isCollision(self.ball, self.player):
            self.bounce(self.ball, self.findHitside(self.ball, self.player))

        # ball collision -- block
        for block in self.blocks:
            if self.isCollision(self.ball, block):
                self.bounce(self.ball, self.findHitside(self.ball, block))
                cast(list, self.blocks).remove(block)
                break

        # ball movement
        self.ball.x += int(self.ball.direction.x * self.ball.speed * et)
        self.ball.y += int(self.ball.direction.y * self.ball.speed * et)

    def render(self) -> None:
        # -- screen
        sdl2.SDL_SetRenderDrawColor(self.renderer, *Colors.BLACK)
        sdl2.SDL_RenderClear(self.renderer)

        # -- block
        for item in self.renderables:
            if isinstance(item, Iterable):
                for subitem in item:
                    subitem.render(self.renderer)
            elif isinstance(item, IRenderable):
                item.render(self.renderer)

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
            self.update(et)
            self.render()

        # render
        sdl2.SDL_DestroyRenderer(self.renderer)
        sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()


main = Main()
main.run()
