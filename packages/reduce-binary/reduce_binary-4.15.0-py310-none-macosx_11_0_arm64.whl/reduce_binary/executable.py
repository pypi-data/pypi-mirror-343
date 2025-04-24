import os
import subprocess
from os import PathLike
from pathlib import Path

BIN_DIR = Path(__file__).parent / "bin"
if os.name == "nt":
    REDUCE_BIN_PATH = BIN_DIR / "reduce.exe"
else:
    REDUCE_BIN_PATH = BIN_DIR / "reduce"


def run_reduce(*args, **kwargs):
    if len(args) > 0:
        cmd_args = args[0]
        args = args[1:]
    else:
        cmd_args = None

    if cmd_args is None or (isinstance(cmd_args, str) and cmd_args == ""):
        return subprocess.run(REDUCE_BIN_PATH, *args, **kwargs)
    elif isinstance(cmd_args, (str, bytes, PathLike)):
        return subprocess.run([REDUCE_BIN_PATH, cmd_args], *args, **kwargs)
    return subprocess.run([REDUCE_BIN_PATH, *cmd_args], *args, **kwargs)


def popen_reduce(
    *args,
    **kwargs,
):
    if len(args) > 0:
        cmd_args = args[0]
        args = args[1:]
    else:
        cmd_args = None

    if cmd_args is None or (isinstance(cmd_args, str) and cmd_args == ""):
        return subprocess.Popen(REDUCE_BIN_PATH, *args, **kwargs)
    elif isinstance(cmd_args, (str, bytes, PathLike)):
        return subprocess.Popen([REDUCE_BIN_PATH, cmd_args], *args, **kwargs)
    return subprocess.Popen([REDUCE_BIN_PATH, *cmd_args], *args, **kwargs)
