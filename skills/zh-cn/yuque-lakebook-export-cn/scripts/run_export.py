from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import venv


SCRIPT_DIR = Path(__file__).resolve().parent
CACHE_VENV = Path.home() / ".agents" / "cache" / "yuque-lakebook-export" / ".venv"
CLI_PATH = SCRIPT_DIR / "cli.py"
REQUIREMENTS_PATH = SCRIPT_DIR / "requirements.txt"


def venv_python_path() -> Path:
    if os.name == "nt":
        return CACHE_VENV / "Scripts" / "python.exe"
    return CACHE_VENV / "bin" / "python"


def ensure_venv() -> Path:
    python_path = venv_python_path()
    if python_path.exists():
        return python_path
    CACHE_VENV.parent.mkdir(parents=True, exist_ok=True)
    venv.EnvBuilder(with_pip=True).create(CACHE_VENV)
    return python_path


def ensure_dependencies(python_path: Path) -> None:
    check_cmd = [
        str(python_path),
        "-c",
        "import bs4, yaml, requests",
    ]
    result = subprocess.run(check_cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return
    install_cmd = [
        str(python_path),
        "-m",
        "pip",
        "install",
        "-r",
        str(REQUIREMENTS_PATH),
    ]
    subprocess.run(install_cmd, check=True)


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
    print("错误：必须提供输出根目录。请先向用户确认导出位置，再传入 -o/--output。", file=sys.stderr)
    raise SystemExit(2)


def main() -> int:
    ensure_output_argument()
    python_path = ensure_venv()
    ensure_dependencies(python_path)
    os.execv(str(python_path), [str(python_path), str(CLI_PATH), *sys.argv[1:]])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
