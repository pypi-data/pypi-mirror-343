from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable, NoReturn
from importlib.metadata import distribution

__version__ = "1.05.00"  # Match pyproject.toml

swashes_executable_path_base = None
try:
    swashes_files = distribution("swashes").files
    if swashes_files:
        # Look for the executable based on wheel.install-dir = "swashes/data"
        # and the expected install location 'bin/swashes' from CMake.
        expected_prefix = "swashes/data/bin/swashes"
        for script in swashes_files:
            if str(script).startswith(expected_prefix):
                resolved_script = Path(script.locate()).resolve(strict=True)
                # parent[0]=bin, parent[1]=data. We want the 'data' dir.
                swashes_executable_path_base = resolved_script.parents[1]
                break
except ImportError:
    pass  # Package might not be installed yet

SWASHES_DATA = swashes_executable_path_base

assert SWASHES_DATA is not None, "Could not determine SWASHES_DATA directory"
assert SWASHES_DATA.exists(), f"SWASHES_DATA directory '{SWASHES_DATA}' not found"

SWASHES_BIN_DIR = SWASHES_DATA / "bin"


def _program(name: str, args: Iterable[str]) -> int:
    """Minimal subprocess.call wrapper (for Windows)."""
    # Add .exe suffix for Windows executable name
    executable_name = f"{name}.exe" if sys.platform.startswith("win") else name
    return subprocess.call([SWASHES_BIN_DIR / executable_name, *args], close_fds=False)


def _program_exit(name: str, *args: str) -> NoReturn:
    """Minimal os.execl wrapper (for Unix)."""
    # Add .exe suffix for Windows executable name
    executable_name = f"{name}.exe" if sys.platform.startswith("win") else name
    executable_path = SWASHES_BIN_DIR / executable_name
    try:
        os.execl(executable_path, executable_path, *args)
    except OSError as e:
        # Basic error handling if execl fails
        print(f"Error executing swashes: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> NoReturn:
    """Entry point mapped to the 'swashes' command."""
    if sys.platform.startswith("win"):
        # Use subprocess.call on Windows and exit with its return code
        raise SystemExit(_program("swashes", sys.argv[1:]))
    else:
        # Use os.execl on Unix-like systems
        _program_exit("swashes", *sys.argv[1:])
