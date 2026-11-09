"""Checks for a tic-tac-toe BOARD.txt.

The workshop template is three lines. Each line has three cells separated by
one space. A cell is X, O, or . (empty). X always moves first.

Pictures in the tests below are boards. `board()` only removes the indent
used to keep those pictures lined up in this file.
"""

from pathlib import Path
from textwrap import dedent

import pytest

BOARD_PATH = Path(__file__).with_name("BOARD.txt")
EMPTY = "."


def board(picture: str) -> str:
    """Turn an indented picture into the text of a board file."""
    return dedent(picture).strip("\n") + "\n"


def parse_board(text: str) -> list[list[str]]:
    """Return a 3 by 3 grid, or raise ValueError when the layout is wrong."""
    lines = text.splitlines()
    if len(lines) != 3:
        raise ValueError(f"layout: the board must have 3 rows, found {len(lines)}")
    grid: list[list[str]] = []
    for row_number, line in enumerate(lines, start=1):
        cells = line.split(" ")
        if len(cells) != 3 or any(len(cell) != 1 for cell in cells):
            raise ValueError(
                "layout: each row must be three cells separated by one space "
                f"(row {row_number} is {line!r})"
            )
        grid.append(cells)
    return grid


def winning_marks(grid: list[list[str]]) -> set[str]:
    """Return every mark that has three in a row."""
    lines = list(grid)
    for column in range(3):
        lines.append([grid[row][column] for row in range(3)])
    lines.append([grid[index][index] for index in range(3)])
    lines.append([grid[index][2 - index] for index in range(3)])

    winners: set[str] = set()
    for line in lines:
        mark = line[0]
        if mark in {"X", "O"} and line[1] == mark and line[2] == mark:
            winners.add(mark)
    return winners


def validate(text: str) -> None:
    """Raise ValueError when the board breaks a rule."""
    grid = parse_board(text)
    cells = [cell for row in grid for cell in row]
    for cell in cells:
        if cell in {"x", "o"}:
            raise ValueError(f"lowercase x or o is not allowed, found {cell!r}")
        if cell == "0":
            raise ValueError("the digit 0 is not the letter O")
        if cell not in {"X", "O", EMPTY}:
            raise ValueError(f"a cell must be only X, O, or a dot, found {cell!r}")

    x_count = cells.count("X")
    o_count = cells.count("O")
    difference = x_count - o_count
    if difference not in (0, 1):
        raise ValueError(
            "X moves first, so count(X) - count(O) must be 0 or 1 "
            f"(found {x_count} X and {o_count} O)"
        )

    winners = winning_marks(grid)
    if len(winners) > 1:
        raise ValueError("at most one winner")
    if winners == {"X"} and difference != 1:
        raise ValueError(
            "no moves after the game is won: X won, so count(X) - count(O) must be 1 "
            f"(found {x_count} X and {o_count} O)"
        )
    if winners == {"O"} and difference != 0:
        raise ValueError(
            "no moves after the game is won: O won, so count(X) - count(O) must be 0 "
            f"(found {x_count} X and {o_count} O)"
        )


def test_repository_board_is_a_valid_mid_game() -> None:
    """The BOARD.txt in this repository is a legal game still in progress."""
    text = BOARD_PATH.read_text(encoding="utf-8")
    validate(text)
    grid = parse_board(text)
    cells = [cell for row in grid for cell in row]
    assert "X" in cells
    assert "O" in cells
    assert EMPTY in cells
    assert winning_marks(grid) == set()


@pytest.mark.parametrize(
    "text",
    [
        pytest.param(
            board(
                """
                . . .
                . . .
                . . .
                """
            ),
            id="empty-template",
        ),
        pytest.param(
            board(
                """
                X . .
                . . .
                . . .
                """
            ),
            id="x-moves-first",
        ),
        pytest.param(
            board(
                """
                X . O
                . X .
                . . .
                """
            ),
            id="mid-game",
        ),
        pytest.param(
            board(
                """
                X X X
                O O .
                . . .
                """
            ),
            id="x-wins",
        ),
        pytest.param(
            board(
                """
                O O O
                X X .
                X . .
                """
            ),
            id="o-wins",
        ),
        pytest.param(
            board(
                """
                X X X
                X O O
                X O O
                """
            ),
            id="x-wins-on-two-lines",
        ),
        pytest.param(
            board(
                """
                X O X
                X O O
                O X X
                """
            ),
            id="draw",
        ),
    ],
)
def test_valid_boards_are_accepted(text: str) -> None:
    """A legal board is accepted, including a finished game and a draw."""
    validate(text)


@pytest.mark.parametrize(
    "text",
    [
        pytest.param(
            board(
                """
                . . .
                . . .
                """
            ),
            id="two-rows",
        ),
        pytest.param(
            board(
                """
                . . .
                . . .
                . . .
                . . .
                """
            ),
            id="four-rows",
        ),
        pytest.param(
            board(
                """
                . .
                . . .
                . . .
                """
            ),
            id="short-row",
        ),
        pytest.param(
            board(
                """
                . . . .
                . . .
                . . .
                """
            ),
            id="long-row",
        ),
        pytest.param(
            board(
                """
                .  . .
                . . .
                . . .
                """
            ),
            id="double-space",
        ),
        pytest.param(
            board(
                """
                 . . .
                . . .
                . . .
                """
            ),
            id="leading-space",
        ),
    ],
)
def test_board_keeps_the_template_layout(text: str) -> None:
    """The file keeps three rows of three cells separated by one space."""
    with pytest.raises(ValueError, match="layout"):
        validate(text)


@pytest.mark.parametrize(
    "text",
    [
        pytest.param(
            board(
                """
                ? . .
                . . .
                . . .
                """
            ),
            id="question-mark",
        ),
        pytest.param(
            board(
                """
                1 . .
                . . .
                . . .
                """
            ),
            id="digit-one",
        ),
    ],
)
def test_cells_are_only_x_o_or_empty(text: str) -> None:
    """A cell is X, O, or the template's empty marker, a dot."""
    with pytest.raises(ValueError, match="only X, O, or a dot"):
        validate(text)


@pytest.mark.parametrize(
    "text",
    [
        pytest.param(
            board(
                """
                x . .
                . . .
                . . .
                """
            ),
            id="lowercase-x",
        ),
        pytest.param(
            board(
                """
                X . o
                . . .
                . . .
                """
            ),
            id="lowercase-o",
        ),
    ],
)
def test_lowercase_marks_are_rejected(text: str) -> None:
    """Lowercase x and o are not marks. The template uses X and O."""
    with pytest.raises(ValueError, match="lowercase"):
        validate(text)


@pytest.mark.parametrize(
    "text",
    [
        pytest.param(
            board(
                """
                X . 0
                . . .
                . . .
                """
            ),
            id="zero-instead-of-o",
        ),
        pytest.param(
            board(
                """
                X O .
                . X 0
                . . .
                """
            ),
            id="zero-on-a-later-move",
        ),
    ],
)
def test_digit_zero_is_rejected(text: str) -> None:
    """The digit 0 is not the letter O."""
    with pytest.raises(ValueError, match="digit 0"):
        validate(text)


@pytest.mark.parametrize(
    "text",
    [
        pytest.param(
            board(
                """
                O . .
                . . .
                . . .
                """
            ),
            id="o-moves-first",
        ),
        pytest.param(
            board(
                """
                X . X
                . . .
                . . .
                """
            ),
            id="two-x-moves-in-a-row",
        ),
        pytest.param(
            board(
                """
                O . O
                X . .
                . . .
                """
            ),
            id="o-ahead-of-x",
        ),
    ],
)
def test_x_moves_first(text: str) -> None:
    """X moves first, so count(X) minus count(O) is 0 or 1."""
    with pytest.raises(ValueError, match="X moves first"):
        validate(text)


@pytest.mark.parametrize(
    "text",
    [
        pytest.param(
            board(
                """
                X X X
                O O O
                . . .
                """
            ),
            id="both-win-a-row",
        ),
        pytest.param(
            board(
                """
                X O X
                X O .
                X O .
                """
            ),
            id="both-win-a-column",
        ),
    ],
)
def test_at_most_one_winner(text: str) -> None:
    """Both players have three in a row, so the board is rejected."""
    with pytest.raises(ValueError, match="at most one winner"):
        validate(text)


@pytest.mark.parametrize(
    "text",
    [
        pytest.param(
            board(
                """
                X X X
                O O .
                . . O
                """
            ),
            id="o-plays-after-x-wins",
        ),
        pytest.param(
            board(
                """
                O O O
                X X .
                X . X
                """
            ),
            id="x-plays-after-o-wins",
        ),
    ],
)
def test_no_moves_after_a_win(text: str) -> None:
    """If X won, X−O is 1. If O won, X−O is 0."""
    with pytest.raises(ValueError, match="no moves after"):
        validate(text)
