class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, v2: "Vector") -> "Vector":
        return Vector(x=self.x + v2.x, y=self.y + v2.y)

    def __sub__(self, v2: "Vector") -> "Vector":
        return Vector(x=self.x - v2.x, y=self.y - v2.y)

    def __mul__(self, s: int | float) -> "Vector":
        return Vector(x=s * self.x, y=s * self.y)

    def __str__(self) -> str:
        return f"[{self.x},{self.y}]"
