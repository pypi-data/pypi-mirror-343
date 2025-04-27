import random


def random_empty_cell(grid):
    while 1:
        x = random.randint(0, len(grid[0]) - 1)
        y = random.randint(0, len(grid) - 1)
        if grid[y][x] == 0:
            return x, y


def random_state_array():
    grid = [[0 for _ in range(6)] for _ in range(6)]

    PIECES = ["w", "b"]
    N_OF_PIECES = 4

    for piece in PIECES:
        for _ in range(N_OF_PIECES):
            x, y = random_empty_cell(grid)
            grid[y][x] = piece

    return grid


def random_lbp():
    arry = random_state_array()
    print(arry)
    lbp = ""
    c = 0
    for y in arry:
        for sym in y:
            if sym in ["w", "b"]:
                if c > 0:
                    lbp += str(c)
                    c = 0
                lbp += sym
            elif sym == 0:
                c = c + 1

        if c > 0:
            lbp += str(c)
            c = 0
        lbp += "/"

    return lbp.rstrip("/")
