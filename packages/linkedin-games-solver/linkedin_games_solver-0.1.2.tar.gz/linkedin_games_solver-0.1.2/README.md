# LinkedIn-Games-Solver

A Python package designed to solve LinkedIn's puzzle games, including Tango, Queens, and Zip. This tool uses Selenium to automate gameplay, solving each game efficiently by navigating the game board, avoiding obstacles, and following game rules.

Uses Selenium to open a Safari browser, read today's game board, solve it, and input the correct answer.

Find the package on PyPi here: https://pypi.org/project/linkedin-games-solver/

## Usage

Install package: `pip install linkedin-games-solver`

Run in command line: `linkedin-solver`

Or use in Python:

`from linkedin_games_solver import solver`
`solver.main()`

## Supported Games:

Tango: Fill a grid with Moon and Sun symbols according to specific rules.

Queens: Place queens on a chessboard.

Zip: Find a path between sequential numbers in a grid while avoiding walls and covering every square.
