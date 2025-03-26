import math
from typing import List
from Vector import Vector


def x_y_finder(theta: float) -> Vector:
    x: float = 0
    y: float = 0

    # right side
    if (theta >= 0 and theta < math.pi / 4) or (
        theta >= 7 * math.pi / 4 and theta < 8 * math.pi / 4
    ):
        x = 1.0
        y = round(math.tan(theta), 2)

    # top side
    elif theta >= math.pi / 4 and theta < 3 * math.pi / 4:
        x = round(1 / math.tan(theta), 2)
        y = 1.0

    # left side
    elif theta >= 3 * math.pi / 4 and theta < 5 * math.pi / 4:
        x = -1.0
        y = round(math.tan(theta), 2)

    # bottom side
    elif theta >= 5 * math.pi / 4 and theta < 7 * math.pi / 4:
        x = round(1 / math.tan(theta), 2)
        y = -1.0

    return Vector(x, y)


ang = 7 * math.pi / 4
print(x_y_finder(ang))
