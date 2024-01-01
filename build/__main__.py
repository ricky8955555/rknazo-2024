import os
from pathlib import Path
from typing import Any
from build import flag as flagutils, start
from build import build, solver

import shutil

from build.buildinfo import Context, MakeDaemon


working_dir = Path(os.getcwd())

data_path = working_dir / "data"
out_path = working_dir / "out"
utils_path = out_path / ".utils"

out_path.mkdir(exist_ok=True)
utils_path.mkdir(exist_ok=True)

daemons: list[dict[str, Any]] = []


def wrap_make_daemon(working_dir: str | Path) -> MakeDaemon:
    def wrapper(args: list[str], cwd: str | Path | None = None) -> None:
        daemons.append({"args": args, "cwd": str(cwd or working_dir)})
    return wrapper


def main():
    with open(data_path / "magic.txt", "rb") as fp:
        magic_bytes = fp.read()
    with open(data_path / "result.txt", "rb") as fp:
        result = fp.read()

    flags = flagutils.generate_flags(result, magic_bytes)

    flagutils.validate_flags(result, flags, magic_bytes)
    solver.validate_flags(result, flags, magic_bytes)

    for i, flag in enumerate(flags, 1):
        root = working_dir / "challenges" / str(i)
        assert root.exists(), f"challenge {i} does not exists."
        metadata = build.get_metadata(root)
        context = Context(
            flag=flag,
            make_daemon=wrap_make_daemon(Path("challenges") / f"{i}_{metadata.name}"),
        )
        build.build(
            context, root, out_path / "challenges" / f"{i}_{metadata.name}"
        )

    shutil.copytree(working_dir / "solver", utils_path / "solver")

    solver.generate_solver_context(
        magic_bytes, len(flags), utils_path / "solver" / "context.py"
    )

    start.generate_script(daemons, utils_path / "start.py", ["/bin/sh"])

try:
    main()
except Exception:
    shutil.rmtree(out_path)
    raise
