# Agent notes

This file is for coding agents. `README.md` is the guide for people.

This repository is the reference outcome for slot 2 of the Git tic-tac-toe workshop. It holds one mid-game `BOARD.txt` and the pytest check that decides whether a board is valid.

## Board rules

- Keep the template layout: three rows, three cells on a row, one space between cells.
- A cell is `X`, `O`, or `.` (empty).
- Reject lowercase `x` and `o`.
- Reject the digit `0` where the letter `O` belongs.
- X moves first, so count(X) − count(O) is 0 or 1.
- At most one winner.
- No moves after a win: if X won, X−O is 1; if O won, X−O is 0.

The rules live in `tests/test_board.py`. Test files live in `tests/`, are named `test_<name>.py`, and each test function starts with `test_`. If you change a board rule on `main`, update the tests in the same change.

## Before you commit

Run `uv run pytest` and keep that command passing.
