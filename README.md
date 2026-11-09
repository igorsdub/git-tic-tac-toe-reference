# Git tic-tac-toe reference

This is the reference repository for slot 2 of the [Git tic-tac-toe workshop](https://igorsdub.github.io/git-tic-tac-toe-workshop/). It shows one finished outcome: a mid-game board and a small check that decides whether that board is valid.

Pairs play by editing `BOARD.txt` in a copy of the [template](https://github.com/igorsdub/git-tic-tac-toe-template). The template board is three rows of `. . .`. A move replaces one `.` with `X` or `O`. Look here after your own rules, check, and docs exist.

`BOARD.txt` in this repository is a game in progress: X and O have each played twice, and nobody has three in a row.

## Run the check

```bash
uv run pytest
```

That command passes on the board in this repository. It fails when the board breaks a rule. Try a lowercase mark, a digit `0` where a letter `O` belongs, or two X moves in a row, then put the board back.

## Reproducibility

Someone else can run the same check because the project records what it needs and the exact versions.

| Piece | Where it lives | What it does |
| --- | --- | --- |
| Manifest | `pyproject.toml` | Says what the project needs (Python 3.10 or newer, and pytest). |
| Lock file | `uv.lock` | Records the exact versions. |
| Runner | `uv` | Builds the environment and runs the command. |
| Test module | `pytest` | Runs `test_board.py`. |

Julia records the same idea in `Project.toml` and `Manifest.toml`. R records it with `renv`.

## What each file is for

- `BOARD.txt` is the board under test, in the template layout.
- `test_board.py` is one small test for each board rule, plus a test of this repository's board.
- `pyproject.toml` is the manifest. Pytest is a dev dependency, so `uv run pytest` can install and run it.
- `uv.lock` is the lock file `uv` generated.
- `AGENTS.md` is a short brief for a coding agent.
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
