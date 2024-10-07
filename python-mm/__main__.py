import sys
import random
from typing import Self
import readchar
import colorama


class MindRow:
    """MasterMind number row"""

    numbers: list[int]  # Numbers on this row
    used: dict[int]  # If number can be found in this dictionary it is already used

    def __init__(self, numbers: list[int] | None = None) -> None:
        """Create row from a list. If none is provided a random list is created."""
        if numbers is None:
            numbers = list(range(1, 6))
            random.shuffle(numbers)
        self.numbers = numbers
        self.used = {}
        for number in numbers:
            self.used[number] = True

    def len(self) -> int:
        """Return the number of elements in the row."""
        return len(self.numbers)

    def append(self, number: int) -> bool:
        """Try to add a number to the end. Return `True` if succesful."""
        if number < 1 or number > 5:
            return False
        if self.len() >= 5 or number in self.used:
            return False
        self.numbers.append(number)
        self.used[number] = True
        return True

    def remove_last(self) -> bool:
        """Try to remove the last number. Return `True` if succesful."""
        if not len(self.numbers):
            return False
        number = self.numbers.pop()
        del self.used[number]
        return True

    def hits(self, other: Self) -> bool:
        """Compare two rows and return the number of same elements in same places."""
        hits = 0
        for i in range(5):
            if self.numbers[i] == other.numbers[i]:
                hits = hits + 1
        return hits


class MindOutput:
    """Print things to STDOUT."""

    COLORS: list[int] = [90, 94, 92, 93, 91]

    def print_number(number: int) -> None:
        """Print out number."""
        print(
            f"\033[1;7;{MindOutput.COLORS[number - 1]}m {number} \033[0m",
            end="",
            flush=True,
        )

    def erase_number() -> None:
        """Remove last number."""
        print("\b\b\b   \b\b\b", end="", flush=True)

    def advance_row(hits: int) -> None:
        """Print number of hits and advance to a next row."""
        print(f" {hits}\r ")

    def prompt() -> None:
        """Print a prompt."""
        print("> ", end="", flush=True)

    def exit(message: str, code: int = 0) -> None:
        """Print a message and exit program."""
        print(f"\r\033[K  {message}")
        sys.exit(code)


def guess_a_row() -> MindRow:
    """Guess a single row."""
    guess = MindRow([])
    while True:
        input = readchar.readchar()
        match input:
            case "\n" | "\r":
                if guess.len() == 5:
                    return guess
            case "\b" | "\x7f":
                if guess.remove_last():
                    MindOutput.erase_number()
            case "1" | "2" | "3" | "4" | "5":
                input = int(input)
                if guess.append(input):
                    MindOutput.print_number(input)
            case "q" | "\x03":
                MindOutput.exit("Quitting...", 1)


def play() -> None:
    """Play a game."""
    secret = MindRow()
    while True:
        MindOutput.prompt()
        guess = guess_a_row()
        hits = secret.hits(guess)
        MindOutput.advance_row(hits)
        if hits == 5:
            MindOutput.exit("Correct")


colorama.init()
play()
