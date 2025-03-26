from IState import IState
from IRenderable import IRenderable
from typing import Iterable, List, cast
from Block import Block
from Player import Player
from Ball import Ball
from GameObject import GameObject
import Colors
import math
import sdl2
import ctypes
from StateMachine import StateMachine, StateCode
from enum import Enum
from Vector import Vector


class Hitside(Enum):
    top = "top"
    bottom = "bottom"
    left = "left"
    right = "right"


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

        self.reset()

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

    def processEvents(self, event: sdl2.SDL_Event) -> bool:
        while sdl2.SDL_PollEvent(ctypes.byref(event)):
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    self.fsm.changeState(StateCode.INTRO)
        return False

    def update(self, et: int) -> None:
        # handle keyboard input to move player, if within playfield
        currentKeyStates = sdl2.SDL_GetKeyboardState(None)
        if currentKeyStates[sdl2.SDL_SCANCODE_LEFT]:
            if not self.player.x - (0.5 * self.player.w) <= 0:
                self.player.x -= int(self.player.speed * et)

        if currentKeyStates[sdl2.SDL_SCANCODE_RIGHT]:
            if not self.player.x + (0.5 * self.player.w) >= self.screen_width:
                self.player.x += int(self.player.speed * et)

        # ball collision -- wall

        if self.ball.x >= self.screen_width:
            self.ball.direction.x *= -1
            self.ball.x -= int(self.ball.w * 0.5)

        if self.ball.x <= 0:
            self.ball.direction.x *= -1
            self.ball.x += int(self.ball.w * 0.5)

        if self.ball.y >= self.screen_height:
            self.fsm.changeState(StateCode.INTRO)

        if self.ball.y <= 0:
            self.ball.direction.y *= -1
            self.ball.y += int(self.ball.h * 0.5)

        # ball collision -- player
        if self.isCollision(self.ball, self.player):
            self.bounce_bat(self.ball, self.player)

        # ball collision -- block
        for block in self.blocks:
            if self.isCollision(self.ball, block):
                self.bounce_block(self.ball, self.findHitside(self.ball, block))
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

    def vectorise_deg(self, theta: float) -> Vector:
        x: float = 0
        y: float = 0

        # --- IF BALL HITS FROM ABOVE ---
        if theta < 0:
            theta *= -1

            # ang from bat to ball
            theta = theta * 180 / math.pi

            # special angles
            if theta == 0:
                x = 1.0
                y = 0.0

            elif theta == 90:
                x = 0.0
                y = 1.0

            elif theta == 180:
                x = -1.0
                y = 0.0

            # top-right arc
            elif (theta >= 0 and theta < 45) or (theta >= 315 and theta < 360):
                x = 1.0
                y = math.tan(theta * math.pi / 180)

            # top-center arc
            elif theta >= 45 and theta < 135:
                x = 1 / math.tan(theta * math.pi / 180)
                y = 1.0

            # top-left arc
            elif theta >= 135 and theta < 225:
                x = -1.0
                y = math.tan(-1 * theta * math.pi / 180)

        # --- IF BALL HITS FROM BELOW ---
        else:
            theta = 2 * math.pi - theta

            # ang from bat to ball
            theta = theta * 180 / math.pi

            # special angles
            if theta == 0:
                x = 1.0
                y = 0.0

            elif theta == 180:
                x = -1.0
                y = 0.0

            elif theta == 270:
                x = 0.0
                y = -1.0

            # bottom-right arc
            elif (theta >= 0 and theta < 45) or (theta >= 315 and theta < 360):
                x = 1.0
                y = math.tan(theta * math.pi / 180)

            # bottom-left arc
            elif theta >= 135 and theta < 225:
                x = -1.0
                y = math.tan(-1 * theta * math.pi / 180)

            # bottom-center arc
            elif theta >= 225 and theta < 315:
                x = -1 * 1 / math.tan(theta * math.pi / 180)
                y = -1.0

        return Vector(x, -y)

    def bounce_bat(self, ball: Ball, obstacle: GameObject) -> None:
        dy: int = ball.y - obstacle.y
        dx: int = ball.x - obstacle.x
        theta: float = math.atan2(dy, dx)
        bounce_vector: Vector = self.vectorise_deg(theta)

        # trapped ball bug fix and gameplay tuning
        if abs(bounce_vector.x) < 0.2:
            if bounce_vector.x > 0:
                bounce_vector.x = 0.2
            else:
                bounce_vector.x = -0.2

        if abs(bounce_vector.y) < 0.2:
            if bounce_vector.y > 0:
                bounce_vector.y = 0.2
            else:
                bounce_vector.y = -0.2

        ball.direction = bounce_vector
        ball.speed = 0.3 + ((abs(bounce_vector.x) + abs(bounce_vector.y)) / 2) * 0.25

    def bounce_block(self, x: Ball, hitside: Hitside) -> None:
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
