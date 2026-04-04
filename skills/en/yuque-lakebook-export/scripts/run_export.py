from __future__ import annotations

import os
from pathlib import Path
import sys


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
CLI_PATH = SCRIPT_DIR / "cli.py"


def ensure_output_argument() -> None:
    args = sys.argv[1:]
    for index, arg in enumerate(args):
        if arg in {"-o", "--output"}:
            if index + 1 < len(args) and args[index + 1].strip():
                return
            break
        if arg.startswith("--output="):
            if arg.split("=", 1)[1].strip():
                return
            break
    print("Error: output root is required. Confirm the destination with the user and pass -o/--output.", file=sys.stderr)
    raise SystemExit(2)


def main() -> int:
    ensure_output_argument()
    os.execvp(
        "uv",
        [
            "uv",
            "run",
            "--project",
            str(PROJECT_DIR),
            "python",
            str(CLI_PATH),
            *sys.argv[1:],
        ],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
