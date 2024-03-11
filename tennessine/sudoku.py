import pdb

from typing import List


class Sudoku:
    def __init__(self) -> None:
        self.table: List[int] = [0 for _ in range(81)]
        self.generate(0)

    def generate(self, index: int) -> bool:
        y, x = divmod(index, 9)
        available_values: List[int] = self.get_available_values(x, y)
        if index == 81:
            return True
        # backtrace if no available values
        if not available_values:
            return False
        # try all available values
        for available_value in available_values:
            self.table[index] = available_value
            if self.generate(index + 1):
                return True
        # backtrace if no available_values
        self.table[index] = 0
        return False

    def get_available_values(self, x: int, y: int) -> List[int]:
        available_values: List[int] = [i for i in range(1, 10)]
        for index, value in enumerate(self.table):
            j, i = divmod(index, 9)
            if (
                x == i
                or y == j
                or x // 3 * 3 <= i < x // 3 * 3 + 3
                and y // 3 * 3 <= j < y // 3 * 3 + 3
            ) and value in available_values:
                available_values.remove(value)
        return available_values

    def print(self) -> str:
        result: str = ""
        for index, value in enumerate(self.table):
            x = index % 9
            result: str = f"{result} {value}"
            if x == 8:
                result: str = f"{result}\n"
        return result


if __name__ == "__main__":
    sudoku: Sudoku = Sudoku()
    print(sudoku.print())
