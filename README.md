# Master-Mind-Color-Game
A color game made in python, featuring testing


This is a Python implementation of the MasterMind game — a classic color-guessing logic game. The game provides a simple graphical user interface built using Tkinter and separates the game logic (backend) from the interface (frontend) for modularity and testability.

# Game Rules
The program randomly selects 6 distinct colors out of 10.

Your task is to guess the exact combination and order of colors.

After each guess, feedback is given:

Black: Correct color at the correct position.

Grey: Correct color but at the wrong position.

White: Color not in the solution.

You have 20 attempts to solve the puzzle.

# How to Play
1. Launch the game via gameUI.py.

2. Click on the colored buttons to select a color.

3. Use the boxes to assign colors for your guess.

4. Click Submit to check your guess.

5. If you're stuck, click Give Up to reveal the answer.

6. Click Restart to play a new game.

# Design Overview
Backend – master_mind.py
Handles the game mechanics:

Enum classes for Color, Match, GameStatus

Core functions:

select_colors(seed) – randomly selects 6 colors

guess() – compares user guess with the answer

play() – manages game progress, win/loss detection

Frontend – gameUI.py
Handles the user interface:

Tkinter UI with color buttons, selection boxes, and result display

Allows submission, restarting, and giving up
