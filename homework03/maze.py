from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """

    # smeshenia = [(0, -1), (+1, 0)]  # Направления смещения: вниз и вправо
    #
    # for y, el in enumerate(grid):
    #     for x, pos in enumerate(el):
    #         direction = choice((0, 1))
    #
    #         if grid[y][x] == " ":
    #             # Проверка на выход из поля
    #             s_y = y + smeshenia[direction][1]
    #             s_x = x + smeshenia[direction][0]
    #
    #             if (0 <= (s_y) < len(grid)) and (0 <= (s_x) < len(el)):
    #                 grid[y + smeshenia[direction][1]][x + smeshenia[direction][0]] = " "
    #
    #             elif (
    #                 (0 <= (y + smeshenia[(direction + 1) % 2][1]) < len(grid))
    #                 and (0 <= (x + smeshenia[(direction + 1) % 2][0]) < len(el))
    #                 and s_x != 14
    #                 and s_y != 14
    #             ):
    #                 grid[y + smeshenia[(direction + 1) % 2][1]][x + smeshenia[(direction + 1) % 2][0]] = " "
    #
    #             else:
    #                 continue
    directions = [(1, 0), (0, 1)]
    direction = choice(directions)
    if coord[0] - 1 <= 0 and coord[1] + 1 >= len(grid[0]) - 1:
        return grid
    if coord[0] - 1 <= 0:
        direction = (0, 1)
    if coord[1] + 1 >= len(grid[0]) - 1:
        direction = (1, 0)

    if direction == (1, 0):
        grid[coord[0] - 1][coord[1]] = " "
    if direction == (0, 1):
        grid[coord[0]][coord[1] + 1] = " "

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки
    for coord in empty_cells:
        grid = remove_wall(grid, coord)

    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"
    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """

    x_start = y_start = 0
    x_end = y_end = 0

    x_count = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "X":
                x_count += 1
                if x_start == 0 and y_start == 0:
                    x_start = x
                    y_start = y
                else:
                    x_end = x
                    y_end = y
    if x_count < 2:
        return [(y_start, x_start)]

    return [(y_start, x_start), (y_end, x_end)]


def make_step(grid: List[List[Union[str, int]]], k: int):
    """

    :param grid:
    :param k:
    :return:
    """

    def make_num_around(grid: List[List[Union[str, int]]], x: int, y: int):
        ways = [0, 0, 0, 0]
        cheshwnia = [(0, -1), (0, +1), (-1, 0), (+1, 0)]  # Верх, Низ, Лево, Право

        for i in range(4):
            s_y = y + cheshwnia[i][1]
            s_x = x + cheshwnia[i][0]

            if (0 <= (s_y) < len(grid)) and (0 <= (s_x) < len(grid[0])) and grid[s_y][s_x] != "■":

                if grid[s_y][s_x] == 0:
                    grid[s_y][s_x] = k + 1
                else:
                    grid[s_y][s_x] = min(k + 1, grid[s_y][s_x])

                ways[i] = True

        if ways.count(True) > 0:
            return grid, True

        return grid, False

    is_any_changes_on_k = []

    for y, ely in enumerate(grid):
        for x, elx in enumerate(ely):
            if elx == k:
                grid, state = make_num_around(grid, x, y)
                if state:
                    is_any_changes_on_k.append(True)
                else:
                    is_any_changes_on_k.append(False)

    if is_any_changes_on_k.count(True) > 0:
        return grid, True

    return grid, False


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """
    Находит кратчайший путь
    :param grid:
    :param exit_coord:
    :return:
    """

    cheshwnia = [(0, -1), (0, +1), (-1, 0), (+1, 0)]
    way = []
    way.append(exit_coord)

    k = int(grid[exit_coord[0]][exit_coord[1]])

    while k != 1:
        count = 0
        for i in range(4):
            s_y = exit_coord[0] + cheshwnia[i][0]
            s_x = exit_coord[1] + cheshwnia[i][1]

            if (0 <= (s_y) < len(grid)) and (0 <= (s_x) < len(grid[0])) and grid[s_y][s_x] == (k - 1):
                count += 1
                way.append((s_y, s_x))
                k -= 1
                exit_coord = (s_y, s_x)
                break

        if count < 1:
            k += 1
            grid[exit_coord[0]][exit_coord[1]] = " "
            way.pop()
            shortest_path(grid, way[-1])

    #way.append(exit_coord)

    return way


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """
    Проверяет, не в тупике ли мы
    :param grid:
    :param coord:
    :return:
    """

    x, y = coord[0], coord[1]

    if coord in [(0, 0), (0, len(grid[0]) - 1), (len(grid) - 1, 0), (len(grid) - 1, len(grid[0]) - 1)]:
        return True

    if x == 0 and grid[x + 1][y] == "■":
        return True
    if y == 0 and grid[x][y + 1] == "■":
        return True
    if x == len(grid) - 1 and grid[x - 1][y] == "■":
        return True
    if y == len(grid[0]) - 1 and grid[x][y - 1] == "■":
        return True

    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """
    Производит решение лабиринта
    :param grid:
    :return:
    """

    (y_start, x_start), (y_end, x_end) = get_exits(grid)

    # Проверка на то, что вход и выход находятся в одной клетке
    if x_start == x_end and y_start == y_end:
        return grid, (x_start, y_start)

    # Проверка на тупик
    if encircled_exit(grid, (y_start, x_start)) or encircled_exit(grid, (y_end, x_end)):
        return grid, None

    # Поиск пути алгоритмом Дейкстры

    # 1. Ставим нолики и 1
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] != "■":
                grid[y][x] = 0

    grid[y_start][x_start] = 1
    grid[y_end][x_end] = 0

    # 2. Запись длин пути k в пустые ячейки
    k = 1  # Счетчик длины пути
    while grid[y_end][x_end] == 0:
        grid, if_anything_changed_on_k = make_step(grid, k)
        if if_anything_changed_on_k:
            k += 1
        else:
            return grid, None

    # 3. По полученной разметке ищем путь домой
    return grid, shortest_path(grid, (y_end, x_end))


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
                elif grid[i][j] != "■":
                    grid[i][j] = " "
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
