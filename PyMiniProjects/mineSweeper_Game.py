import copy
import random
from math import floor
from operator import contains


class Minesweeper:
    def __init__(self, height, width, difficulty):
        self.height = height
        self.width = width
        self.difficulty = difficulty
        self.view_grid = self.create_visual_grid()
        self.bombs = floor(height * width * 0.15) if difficulty == 1 else (
            floor(height * width * 0.20) if difficulty == 2 else floor(height * width * 0.28)
        )
        self.bomb_grid = None
        self.flagged_cells = set()
        self.first_move_done = False

    def reveal_cells(self, col, row):
        height = self.height
        width = self.width
        bomb_grid = self.bomb_grid
        view_grid = self.view_grid

        if bomb_grid[col][row] == "*":
            return None

        elif bomb_grid[col][row] > 0:
            view_grid[col + 1][row + 1] = f"| {bomb_grid[col][row]} "

        else:
            for i in (
                    range(col - 1, col + 2)
                    if height - 1 > col > 0
                    else (
                            range(col, col + 2)
                            if col == 0
                            else
                            range(col - 1, col + 1)
                    )
            ):
                for j in (
                        range(row - 1, row + 2)
                        if width - 1 > row > 0
                        else (
                                range(row, row + 2)
                                if row == 0
                                else
                                range(row - 1, row + 1))):

                    if view_grid[i + 1][j + 1] != f"| {bomb_grid[i][j]} ":
                        if bomb_grid[i][j] != "*":
                            view_grid[i + 1][j + 1] = f"| {bomb_grid[i][j]} "
                            if bomb_grid[i][j] == 0:
                                self.reveal_cells(i, j)

        return view_grid

    def add_bomb_counts(self, c, r):
        height = self.height
        width = self.width
        bomb_grid = self.bomb_grid

        for i in (
                range(c - 1, c + 2)

                if height - 1 > c > 0
                else (
                        range(c, c + 2)
                        if c == 0
                        else
                        range(c - 1, c + 1)
                )
        ):
            for j in (
                    range(r - 1, r + 2)
                    if width - 1 > r > 0
                    else (
                            range(r, r + 2)
                            if r == 0
                            else
                            range(r - 1, r + 1))):
                if bomb_grid[i][j] != "*":
                    x = int(bomb_grid[i][j])
                    x += 1
                    bomb_grid[i][j] = x

        return bomb_grid

    def create_bomb_grid(self, col=None, row=None):
        height = self.height
        width = self.width
        bombs = self.bombs

        bomb_grid = []

        for i in range(height):
            bomb_grid.append([])
            for j in range(width):
                bomb_grid[i].append(0)

        bomb_pos = []

        while len(bomb_pos) < bombs:
            a = random.randint(0, height - 1)
            b = random.randint(0, width - 1)
            if col is not None and row is not None:
                if ([col - 1, row - 1] == [a, b]
                        or [col, row - 1] == [a, b]
                        or [col + 1, row - 1] == [a, b]
                        or [col - 1, row] == [a, b]
                        or [col, row] == [a, b]
                        or [col + 1, row] == [a, b]
                        or [col - 1, row + 1] == [a, b]
                        or [col, row + 1] == [a, b]
                        or [col + 1, row + 1] == [a, b]
                ):
                    continue
            if [a, b] not in bomb_pos:
                bomb_pos.append([a, b])

        for i in bomb_pos:
            bomb_grid[i[0]][i[1]] = "*"

        self.bomb_grid = bomb_grid

        for i in range(height):
            for j in range(width):
                if bomb_grid[i][j] == "*":
                    self.add_bomb_counts(i, j)

        return bomb_grid




    def create_visual_grid(self):
        height = self.height
        width = self.width

        grid = []

        for i in range(height):
            grid.append([])
            for j in range(width):
                grid[i].append("| _ ")
                if j == width - 1:
                    grid[i].append("|")

        for i in range(height):
            if i < 10:
                grid[i].insert(0, f"{i}  ")
            else:
                grid[i].insert(0, f"{i} ")

        grid.insert(0, ["    "])
        for i in range(width):
            if i < 10:
                grid[0].append(f" {i}  ")
            else:
                grid[0].append(f"{i}  ")

        return grid

    def flag_bomb(self, c, r):
        if not contains(self.view_grid[c+1][r+1].split(" "),"_") and not contains(self.view_grid[c+1][r+1].split(" "),"!"):
            print("\n***cannot flag a revealed cell***")

        elif (c, r) in self.flagged_cells:
            self.flagged_cells.remove((c, r))
            self.view_grid[c + 1][r + 1] = "| _ "
        else:
            self.flagged_cells.add((c, r))
            self.view_grid[c + 1][r + 1] = "| ! "





    def check_win(self):
        # Win if all non-bomb cells are revealed
        for i in range(self.height):
            for j in range(self.width):
                if self.bomb_grid[i][j] != "*" and self.view_grid[i + 1][j + 1] == "| _ ":
                    return False
        return True




    def print_visual_grid(self):
        for i in self.view_grid:
            print("".join(i))

    def run_game_loop(self):
        print("""\n***********\ncorrect input formats :\n "col row" e.g.: 0 0 \n "col row col row ..." to reveal multiple cells e.g.: 0 0 1 1\n"col row !" to flag a bomb e.g.: 0 0 ! \n***********""")

        col,row = 0,0

        # First move (easy start)
        self.print_visual_grid()
        while True:
            inp = input("choose cell: ")
            try:
                parts = inp.split(" ")
                col = int(parts[0])
                row = int(parts[1])
                if not (0 <= col < self.height and 0 <= row < self.width):
                    print(f"invalid input!! \n please enter cell position between 0 and {self.height-1} for col and 0 and {self.width-1} for row")
                    continue
                break
            except (ValueError, IndexError):
                print("invalid input format! Use: col row")
                continue

        self.bomb_grid = self.create_bomb_grid(col, row)
        self.first_move_done = True
        res = self.reveal_cells(col, row)
        if not res:
            print("You revealed a bomb on first move? This should not happen!")
            return

        while True:
            print(f"\n{self.bombs - len(self.flagged_cells)} bombs left")
            self.print_visual_grid()
            inp = input("choose cell: ")
            try:
                parts = inp.split(" ")
                if len(parts) < 2:
                    print("invalid input!! Please enter at least 'col row'")
                    continue
                col = int(parts[0])
                row = int(parts[1])
                if not (0 <= col < self.height and 0 <= row < self.width):
                    print(f"invalid input!! \n please enter cell position between 0 and {self.height - 1} for col and 0 and {self.width - 1} for row")
                    continue

                if len(parts) == 3 and parts[2] == "!":
                    self.flag_bomb(col, row)
                else:
                    res = self.reveal_cells(col, row)
                    if not res:
                        print("you revealed a bomb...\n game over\n")
                        break

                    if self.check_win():
                        self.print_visual_grid()
                        print("Congratulations! You won the game!")
                        break

            except ValueError:
                print("""invalid input!! \n please enter cell position in this format "col row" or "col row !" for flagging a cell""")
                continue
            except IndexError:
                print(f"""invalid input!! \n please enter cell position between 0 and {self.height - 1} for col and 0 and {self.width - 1} for row""")
                continue


def main():
    while True:  # grid dimensions and difficulty
        try:
            height = int(input("choose table height:"))
            width = int(input("choose table width:"))
            difficulty = int(input("choose difficulty: 1 for easy, 2 for medium, 3 for hard:"))
            if height <= 0 or width <= 0 or difficulty not in (1, 2, 3):
                raise ValueError
            break
        except ValueError:
            print("Please enter valid positive integers for height and width, and difficulty 1, 2, or 3.")

    game = Minesweeper(height, width, difficulty)
    game.run_game_loop()

    print("Thanks for playing Minesweeper!")


if __name__ == "__main__":
    main()
