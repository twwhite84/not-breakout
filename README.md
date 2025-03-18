# Not Breakout

This is a game similar to the old arcade title Breakout. I wrote it as an exercise in learning SDL and refreshing my knowledge of Python from my university data science courses. Some of the things it demonstrates include:
- Use of typed code and the static type checker Mypy 
- Classes and interfaces (abstract base class and methods... similar to pure virtual methods in C++)
- Use of ctypes and byref to work with pointer types in the C-based library SDL
- Operator overloading for a 2D Vector class
- Use of a state pattern to implement switching between intro and game states

To run:
- Clone this repo and create a new .venv virtual environment
- Install the packages from the requirements.txt manifest
- python main.py
- Arrow keys to move paddle, Escape to quit

To do:
- Sound fx and proper physics
- Data-driven design (i.e. levels in files, not hardcoded)
- More gameplay variation

![Intro screen](media/intro.png)
![Game screen](media/game.png)
