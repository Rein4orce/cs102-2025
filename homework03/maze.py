from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    row, col = coord
    if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
        grid[row][col] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))
    for cell in empty_cells:
        x, y = cell
        directions = []
        if x > 1:
            directions.append(("up", (x - 1, y)))
        if y < cols - 2:
            directions.append(("right", (x, y + 1)))
        if directions:
            chosen_dir, wall_coord = choice(directions)
            remove_wall(grid, wall_coord)

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    # grid[int(input(x_in))][int(input(y_in))], grid[int(input(x_out))][int(input(y_out))] = "X", "X"
    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    exit_coord = []
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "X":
                exit_coord.append((i, j))
    return exit_coord


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    rows, cols = len(grid), len(grid[0])
    for i in range(rows):
        for j in range(cols):
            cell = grid[i][j]
            if isinstance(cell, int) and cell == k - 1:
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols:
                        neighbor = grid[ni][nj]
                        if isinstance(neighbor, int) and neighbor == 0:
                            grid[ni][nj] = k
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    rows, cols = len(grid), len(grid[0])
    path = [exit_coord]
    current_r, current_c = exit_coord
    if not isinstance(grid[current_r][current_c], int):
        return None
    current_val = int(grid[int(current_r)][int(current_c)])
    if int(grid[int(current_r)][int(current_c)]) <= 0:
        return None
    while current_val > 1:
        found = False
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = current_r + dr, current_c + dc
            if 0 <= nr < rows and 0 <= nc < cols and int(grid[nr][nc]) == current_val - 1:
                path.append((nr, nc))
                current_r, current_c = nr, nc
                current_val -= 1
                found = True
                break
        if not found:
            return None

    path.reverse()
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    row, col = coord
    rows, cols = len(grid), len(grid[0])
    walls_count = 0
    empty_neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols:
            if grid[new_row][new_col] == "■":
                walls_count += 1
            else:
                empty_neighbors.append((new_row, new_col))
        else:
            walls_count += 1

    on_top_bottom = row == 0 or row == rows - 1
    on_left_right = col == 0 or col == cols - 1
    on_border = on_top_bottom or on_left_right
    on_corner = on_top_bottom and on_left_right

    if on_corner and walls_count >= 2:
        return True
    elif on_border and not on_corner and walls_count >= 3:
        return True
    elif on_border and not on_corner and walls_count == 2:
        if empty_neighbors:
            neighbor = empty_neighbors[0]
            neighbor_empty = 0
            for dr, dc in directions:
                nr, nc = neighbor[0] + dr, neighbor[1] + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "■":
                    neighbor_empty += 1
            if neighbor_empty >= 1:
                return False
        return True
    else:
        return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[List[Tuple[int, int]]]]:
    exits = get_exits(grid)
    if len(exits) < 2:
        return grid, None
    start = exits[0]
    end = exits[1]
    rows, cols = len(grid), len(grid[0])
    dist_map: List[List[Union[str, int]]] = []
    for r in range(rows):
        row_map: List[Union[str, int]] = []
        for c in range(cols):
            if grid[r][c] == "■":
                row_map.append(-1)
            elif (r, c) == start:
                row_map.append(1)
            else:
                row_map.append(0)
        dist_map.append(row_map)
    k = 1
    max_iterations = rows * cols
    iterations = 0
    while isinstance(dist_map[end[0]][end[1]], int) and dist_map[end[0]][end[1]] == 0 and iterations < max_iterations:
        k += 1
        old_map = [row[:] for row in dist_map]
        dist_map = make_step(dist_map, k)
        if old_map == dist_map:
            return grid, None
        iterations += 1
    end_cell = dist_map[end[0]][end[1]]
    if not isinstance(end_cell, int) or end_cell == 0:
        return grid, None
    return grid, None


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
