from IState import IState
from IRenderable import IRenderable
from typing import Iterable, List, Union, cast
from Block import Block
from Player import Player
from Ball import Ball
from GameObject import GameObject
from Hitside import Hitside
import Colors
import math
import sdl2
import ctypes
from StateMachine import StateMachine, StateCode


class PlayState(IState):
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
        self.screen_width = self.screen_width_c.value
        self.screen_height = self.screen_height_c.value
        self.renderer = renderer
        self.fsm = fsm

        # blocks
        self.blocks: Iterable[Block] = self.makeBlocks()

        # player
        self.player: Player = Player(
            x=int(self.screen_width * 0.5),
            y=self.screen_height - 50,
            w=100,
            h=20,
            color=Colors.WHITE,
        )

        # ball
        ball_diameter = 20
        self.ball: Ball = Ball(
            x=int(self.screen_width * 0.5),
            y=int(self.screen_height * 0.5 - ball_diameter * 0.5),
            w=ball_diameter,
            h=ball_diameter,
            color=Colors.CYAN,
        )

        self.renderables: Iterable[Union[IRenderable | Iterable[IRenderable]]] = [
            self.blocks,
            self.player,
            self.ball,
        ]

    def reset(self) -> None:
        # blocks
        self.blocks = self.makeBlocks()

        # player
        self.player = Player(
            x=int(self.screen_width * 0.5),
            y=self.screen_height - 50,
            w=100,
            h=20,
            color=Colors.WHITE,
        )

        # ball
        ball_diameter = 20
        self.ball = Ball(
            x=int(self.screen_width * 0.5),
            y=int(self.screen_height * 0.5 - ball_diameter * 0.5),
            w=ball_diameter,
            h=ball_diameter,
            color=Colors.CYAN,
        )

        self.renderables = [
            self.blocks,
            self.player,
            self.ball,
        ]

    def update(self, et: int) -> None:
        # handle keyboard input to move player, if within playfield
        currentKeyStates = sdl2.SDL_GetKeyboardState(None)
        if currentKeyStates[sdl2.SDL_SCANCODE_LEFT]:
            if not self.player.x - (0.5 * self.player.w) <= 0:
                self.player.x -= int(self.player.speed * et)

        if currentKeyStates[sdl2.SDL_SCANCODE_RIGHT]:
            if not self.player.x + (0.5 * self.player.w) >= self.screen_width:
                self.player.x += int(self.player.speed * et)

        if currentKeyStates[sdl2.SDL_SCANCODE_ESCAPE]:
            quitEvent = sdl2.SDL_Event()
            quitEvent.type = sdl2.SDL_QUIT
            sdl2.SDL_PushEvent(ctypes.byref(quitEvent))
            # self.fsm.changeState(StateCode.PLAY, StateCode.INTRO)

        # ball collision -- wall
        if self.ball.x >= self.screen_width:
            self.ball.direction.x *= -1
            self.ball.x -= int(self.ball.w * 0.5)

        if self.ball.x <= 0:
            self.ball.direction.x *= -1
            self.ball.x += int(self.ball.w * 0.5)

        if self.ball.y >= self.screen_height:
            # quitEvent = sdl2.SDL_Event()
            # quitEvent.type = sdl2.SDL_QUIT
            # sdl2.SDL_PushEvent(ctypes.byref(quitEvent))
            self.fsm.changeState(StateCode.PLAY, StateCode.INTRO)

        if self.ball.y <= 0:
            self.ball.direction.y *= -1
            self.ball.y += int(self.ball.h * 0.5)

        # ball collision -- player
        if self.isCollision(self.ball, self.player):
            self.bounce(self.ball, self.findHitside(self.ball, self.player))

        # ball collision -- block
        for block in self.blocks:
            if self.isCollision(self.ball, block):
                self.bounce(self.ball, self.findHitside(self.ball, block))
                cast(list[Block], self.blocks).remove(block)
                break

        # ball movement
        self.ball.x += int(self.ball.direction.x * self.ball.speed * et)
        self.ball.y += int(self.ball.direction.y * self.ball.speed * et)

    def render(self) -> None:
        # -- draw renderables
        for item in self.renderables:
            if isinstance(item, Iterable):
                for subitem in item:
                    subitem.render(self.renderer)
            elif isinstance(item, IRenderable):
                item.render(self.renderer)

    def onEnter(self) -> bool:
        self.reset()
        print("PLAY STATE -- ENTER")
        return True

    def onExit(self) -> bool:
        print("PLAY STATE -- EXIT")
        return True

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
                        int(x_offset + column * (block_width + margin)),
                        int(y_offset + row * (block_height + margin)),
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
            x.y -= int(0.5 * x.h)
            x.direction.y *= -1

        elif hitside == Hitside.bottom:
            x.y += int(0.5 * x.h)
            x.direction.y *= -1

        elif hitside == Hitside.right:
            x.x += int(0.5 * x.w)
            x.direction.x *= -1

        else:
            x.x -= int(0.5 * x.w)
            x.direction.x *= -1
