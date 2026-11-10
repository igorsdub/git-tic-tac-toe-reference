# Git tic-tac-toe reference

This is the reference repository for slot 2 of the [Git tic-tac-toe workshop](https://igorsdub.github.io/git-tic-tac-toe-workshop/). It shows one finished outcome: a mid-game board and a small check that decides whether that board is valid.

Pairs play by editing `BOARD.txt` in a copy of the [template](https://github.com/igorsdub/git-tic-tac-toe-template). The template board is three rows of `. . .`. A move replaces one `.` with `X` or `O`. Look here after your own rules, check, and docs exist.

`BOARD.txt` in this repository is a game in progress: X and O have each played twice, and nobody has three in a row.

## Run the check

```bash
uv run pytest
```

That command passes on the board in this repository. It fails when the board breaks a rule.

## How the tests work

The tests live in `tests/test_board.py`. Run them with `uv run pytest`. Pytest runs every function whose name starts with `test_`. Each `pytest.param` in a test is a separate case. This file has 27 cases.

A case that should pass calls `validate` and expects no error. A case that should fail uses `pytest.raises(ValueError, match=...)`: `validate` must raise `ValueError`, and the message must contain the `match` text.

- `test_repository_board_is_a_valid_mid_game` reads `BOARD.txt`, calls `validate` on it, and asserts the cells include `X`, `O`, and `.`, and that `winning_marks` is empty.
- `test_valid_boards_are_accepted` calls `validate` on an empty board, a single `X`, a mid-game board, an X win, an O win, an X win on two lines, and a draw, and expects no error.
- `test_board_keeps_the_template_layout` expects `ValueError` matching `layout` for two rows, four rows, a row of two cells, a row of four cells, two spaces between cells, and a leading space.
- `test_cells_are_only_x_o_or_empty` expects `ValueError` matching `only X, O, or a dot` for a cell `?` and a cell `1`.
- `test_lowercase_marks_are_rejected` expects `ValueError` matching `lowercase` for a cell `x` and a cell `o`.
- `test_digit_zero_is_rejected` expects `ValueError` matching `digit 0` for a cell `0` on `X . 0`, and for a cell `0` on a board that already has `X` and `O`.
- `test_x_moves_first` expects `ValueError` matching `X moves first` for a lone `O`, for `X . X` with no `O`, and for two `O` marks and one `X`.
- `test_at_most_one_winner` expects `ValueError` matching `at most one winner` for a row `X X X` followed by a row `O O O`, and for a column of `X` together with a column of `O`.
- `test_no_moves_after_a_win` expects `ValueError` matching `no moves after` for an X row plus three `O` marks, and for an O row plus four `X` marks.

## See it fail

`demo/` has three copies of the checked-in board, each broken in one way. Pytest does not collect that folder, and no test reads it until you copy a file onto `BOARD.txt`. Only `test_repository_board_is_a_valid_mid_game` reads `BOARD.txt`, so the other 26 cases still pass.

The traces below are from `uv run pytest` on this repository. A line that is only `...` marks lines left out. The last line is pytest's summary. The seconds there are how long that run took.

### Lowercase `x`

`demo/lowercase-x.txt` changes the first cell from `X` to `x`.

```bash
cp demo/lowercase-x.txt BOARD.txt && uv run pytest
```

```text
tests/test_board.py F..........................                          [100%]
...
__________________ test_repository_board_is_a_valid_mid_game ___________________
...
text = 'x O X\nO . .\n. . .\n'
...
E               ValueError: lowercase x or o is not allowed, found 'x'

tests/test_board.py:63: ValueError
...
========================= 1 failed, 26 passed in 0.02s =========================
```

### Digit `0`

`demo/zero-for-o.txt` changes the top-row `O` to the digit `0`.

```bash
cp demo/zero-for-o.txt BOARD.txt && uv run pytest
```

```text
tests/test_board.py F..........................                          [100%]
...
__________________ test_repository_board_is_a_valid_mid_game ___________________
...
text = 'X 0 X\nO . .\n. . .\n'
...
E               ValueError: the digit 0 is not the letter O

tests/test_board.py:65: ValueError
...
========================= 1 failed, 26 passed in 0.02s =========================
```

### Two moves at once

`demo/two-moves.txt` replaces the two empty cells on the second row with `X`. The board then has 4 `X` marks and 2 `O` marks.

```bash
cp demo/two-moves.txt BOARD.txt && uv run pytest
```

```text
tests/test_board.py F..........................                          [100%]
...
__________________ test_repository_board_is_a_valid_mid_game ___________________
...
text = 'X O X\nO X X\n. . .\n'
...
E           ValueError: X moves first, so count(X) - count(O) must be 0 or 1 (found 4 X and 2 O)

tests/test_board.py:73: ValueError
...
========================= 1 failed, 26 passed in 0.02s =========================
```

### Restore the board

```bash
git checkout BOARD.txt
uv run pytest
```

When `BOARD.txt` has edits, `git checkout BOARD.txt` prints:

```text
Updated 1 path from the index
```

`uv run pytest` then prints:

```text
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.2.0, pluggy-1.7.0
rootdir: /agent/repos/git-tic-tac-toe-reference
configfile: pyproject.toml
collected 27 items

tests/test_board.py ...........................                          [100%]

============================== 27 passed in 0.02s ==============================
```

## Reproducibility

Someone else can run the same check because the project records what it needs and the exact versions.

| Piece | Where it lives | What it does |
| --- | --- | --- |
| Manifest | `pyproject.toml` | Says what the project needs (Python 3.10 or newer, and pytest). |
| Lock file | `uv.lock` | Records the exact versions. |
| Runner | `uv` | Builds the environment and runs the command. |
| Test module | `pytest` | Runs `tests/test_board.py`. |

Julia records the same idea in `Project.toml` and `Manifest.toml`. R records it with `renv`.

## What each file is for

This README is for people.

- `BOARD.txt` is the board under test, in the template layout.
- `demo/` holds three broken boards used above. The tests do not collect or read that folder.
- `tests/test_board.py` is one small test for each board rule, plus a test of this repository's board. Test files live in `tests/`, are named `test_<name>.py`, and each test function starts with `test_`.
- `pyproject.toml` is the manifest. Pytest is a dev dependency, so `uv run pytest` can install and run it.
- `uv.lock` is the lock file `uv` generated.
- `AGENTS.md` is the short note for a coding agent.
- `.pre-commit-config.yaml` is an optional hook with the same check as the guide. After `uvx pre-commit install`, Git runs `uv run pytest` before each commit.
- `.gitignore` keeps `.venv/`, `__pycache__/`, and `.pytest_cache/` out of Git.

GitHub Actions can run this same test on every push. This repository uses the local check above.

## Board rules

- The file keeps the template shape: three rows, three cells, one space between cells.
- A cell is `X`, `O`, or `.`.
- Lowercase `x` and `o` are rejected.
- The digit `0` is rejected. It is not the letter `O`.
- X moves first, so the number of X marks minus the number of O marks is 0 or 1.
- At most one player has three in a row.
- Play stops when someone wins. If X won, X has one more mark than O. If O won, the counts are equal.
