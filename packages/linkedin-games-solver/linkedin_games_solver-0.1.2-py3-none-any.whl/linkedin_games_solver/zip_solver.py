from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import math
from collections import deque
import time

DOWN = 1
RIGHT = 2
LEFT = 3
UP = 4


class ZipSolver:
    game_url = "https://www.linkedin.com/games/zip/"

    def __init__(self, driver):
        self.driver = driver
        self.board, self.walls = self.get_board_and_walls()
        self.print_board()

    def get_board_and_walls(self):
        print("⏳ Setting up board...")
        iframe = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe"))
        )
        self.driver.switch_to.frame(iframe)

        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.ID, "launch-footer-start-button"))
        ).click()

        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "trail-board"))
        )

        cells = self.driver.find_elements(By.CLASS_NAME, "trail-cell")

        grid_size = int(math.sqrt(len(cells)))
        board = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        walls = set()

        for idx, cell in enumerate(cells):
            row = idx // grid_size
            col = idx % grid_size

            cell_value = self.get_cell_value_if_int(cell)
            if cell_value:
                board[row][col] = cell_value

            cell_walls = self.get_cell_walls(cell)

            if RIGHT in cell_walls:
                walls.add((row, col, row, col + 1))
            if DOWN in cell_walls:
                walls.add((row, col, row + 1, col))
            if LEFT in cell_walls:
                walls.add((row, col - 1, row, col))
            if UP in cell_walls:
                walls.add((row - 1, col, row, col))

        return board, walls

    def get_cell_value_if_int(self, cell):
        try:
            inner_div = cell.find_element(By.CSS_SELECTOR, ".trail-cell-content")
            text = inner_div.text.strip()
            if text.isdigit():
                return int(text)
        except NoSuchElementException:
            pass

        return None

    def get_cell_walls(self, cell):
        try:
            inner_divs = cell.find_elements(By.CSS_SELECTOR, ".trail-cell-wall")
            all_walls = set()
            for inner_div in inner_divs:
                inner_div_classes = inner_div.get_attribute("class").split()

                if "trail-cell-wall--right" in inner_div_classes:
                    all_walls.add(RIGHT)
                if "trail-cell-wall--up" in inner_div_classes:
                    all_walls.add(UP)
                if "trail-cell-wall--down" in inner_div_classes:
                    all_walls.add(DOWN)
                if "trail-cell-wall--left" in inner_div_classes:
                    all_walls.add(LEFT)

            return list(all_walls)
        except NoSuchElementException:
            pass

        return []

    def solve_game(self):
        board, walls = self.board, self.walls
        rows, cols = len(board), len(board[0])

        # Build wall set for fast lookups
        wall_set = set((x1, y1, x2, y2) for x1, y1, x2, y2 in walls)        

        # Find positions of numbers 1, 2, 3, ...
        numbered_positions = {}
        max_num = 0
        for x in range(rows):
            for y in range(cols):
                if board[x][y] > 0:
                    numbered_positions[board[x][y]] = (x, y)
                    max_num = max(max_num, board[x][y])

        # Movement directions
        DIRS = [(-1,0), (1,0), (0,-1), (0,1)]

        # BFS to find all paths from start to end, avoiding visited and walls
        def bfs_all_paths(start, end, visited):
            queue = deque()
            queue.append((start, [start]))
            all_paths = []

            while queue:
                (x, y), path = queue.popleft()

                if (x, y) == end:
                    all_paths.append(path)
                    continue

                for dx, dy in DIRS:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols: # on the board
                        # no overlaps from previous paths or this path, no walls,
                        # not hitting a number (other than the one we want to hit)
                        if (nx, ny) not in visited \
                            and (nx, ny) not in path \
                            and not self.is_blocked(wall_set, x, y, nx, ny) \
                            and (self.board[nx][ny] == 0 or (nx, ny) == end):
                            queue.append(((nx, ny), path + [(nx, ny)]))

            return all_paths

        # Backtracking to build the full path from 1 → 2 → 3 → ...
        def backtrack(current_num, visited, path_so_far):
            if current_num == max_num:
                # Check if all cells are visited
                if len(visited) == rows * cols:
                    return path_so_far
                return None

            start = numbered_positions[current_num]
            end = numbered_positions[current_num + 1]

            paths = bfs_all_paths(start, end, visited.copy())

            for path in paths:
                new_visited = visited.union(path)
                full_path = path_so_far + path[1:]  # skip duplicate start
                result = backtrack(current_num + 1, new_visited, full_path)
                if result:
                    return result

            return None

        # Start from the position of 1
        start_pos = numbered_positions[1]
        visited = set([start_pos])
        self.path = backtrack(1, visited, [start_pos])

    def is_blocked(self, wall_set, x1, y1, x2, y2):
        return (x1, y1, x2, y2) in wall_set or (x2, y2, x1, y1) in wall_set
    
    def print_solved_game(self):
        print("-" * 60)
        print("GAME SOLVED")
        print("-" * 60)
        print()
        self.print_board(self.path)

    def print_board(self, path=[]):
        # Define arrow symbols for directions
        arrows = {(0, 1): " → ", (1, 0): " ↓ ", (0, -1): " ← ", (-1, 0): " ↑ "}
        board = self.board

        display = [
            [" " + str(i) + " " if i > 0 else "  " for i in row] for row in board
        ]

        wall_set = set(self.walls)

        rows, cols = len(board), len(board[0])

        for i in range(len(path)):
            x, y = path[i]
            if board[x][y]:
                continue
            elif i + 1 < len(path):
                x2, y2 = path[i + 1]
                dx, dy = x2 - x, y2 - y
                display[x][y] = arrows.get((dx, dy), " ? ")
            else:
                display[x][y] = " • "

        # Print the board with walls
        for x in range(rows):

            # Print the current row and vertical walls
            line = ""
            for y in range(cols):
                if y > 0:
                    if (
                        x,
                        y - 1,
                        x,
                        y,
                    ) in wall_set:  # Check wall between (x,y-1) and (x,y)
                        line += "┃"
                    else:
                        line += " "
                line += f"{display[x][y]}"
            print(line)

            if x < rows:
                line = ""
                for y in range(cols):
                    if (
                        x,
                        y,
                        x + 1,
                        y,
                    ) in wall_set:
                        line += " ━━━"
                    else:
                        line += "    "
                print(line)

    def add_solved_board_to_site(self, delay=0, timeout=0):
        if timeout:
            time.sleep(timeout)
        
        direction_keys = {
            (0, 1): Keys.ARROW_RIGHT,
            (0, -1): Keys.ARROW_LEFT,
            (1, 0): Keys.ARROW_DOWN,
            (-1, 0): Keys.ARROW_UP
        }

        body = self.driver.find_element("tag name", "body")
        for i in range(1, len(self.path)):
            x1, y1 = self.path[i - 1]
            x2, y2 = self.path[i]
            dx, dy = x2 - x1, y2 - y1
            key = direction_keys.get((dx, dy))

            if not key:
                raise ValueError(f"Invalid move from {self.path[i - 1]} to {self.path[i]}")

            body.send_keys(key)
            if delay:
                time.sleep(delay)