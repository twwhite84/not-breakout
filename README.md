# Not Breakout

This is a game similar to the old arcade title Breakout. I wrote it as an exercise in learning SDL and refreshing my knowledge of Python from my university data science courses. It demonstrates the following:
- Use of a static type checker in the form of Mypy
- Classes and interfaces (technically abstract base class with do-nothing methods... similar to pure virtual methods in C++)
- Use of ctypes and byref to work with a C-based library, in this case SDL

To run:
- Create a .venv virtual environment
- Install the packages from the requirements.txt manifest
- python main.py
