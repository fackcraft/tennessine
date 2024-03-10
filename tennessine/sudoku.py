from typing import List

from rich.console import Console

console: Console = Console()


class Sudoku:
    def __init__(self) -> None:
        self.table: List[int] = [0 for _ in range(81)]
        for index in range(81):
            y, x = divmod(index, 9)
            def get_available_value_weight(available_value: int) -> int:
                weight: int = 0
                for index, value in enumerate(self.table):
                    j, i = divmod(index, 9)
                    if (
                        x == i
                        or y == j
                        or x // 3 <= i < x // 3 + 3
                        and y // 3 <= j < y // 3 + 3
                    ) and value == available_value:
                        weight += 1
                return weight
            self.table[index] = min(self.get_available_values(x, y), key=get_available_value_weight)
            console.log(self.get_available_values(x, y))
            console.log(self.print())

    def get_available_values(self, x: int, y: int) -> List[int]:
        available_values: List[int] = [i for i in range(1, 10)]
        for index, value in enumerate(self.table):
            j, i = divmod(index, 9)
            if (
                x == i
                or y == j
                or x // 3 <= i < x // 3 + 3
                and y // 3 <= j < y // 3 + 3
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

