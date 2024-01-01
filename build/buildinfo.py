from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Protocol


class MakeDaemon(Protocol):
    def __call__(
        self, args: list[str], cwd: str | Path | None = None
    ) -> None: ...


@dataclass(frozen=True, kw_only=True)
class Context:
    flag: str
    make_daemon: MakeDaemon


@dataclass(frozen=True, kw_only=True)
class Metadata:
    name: str
    artifact: str | Path
    build: Callable[[], None]
    post: Callable[[], None] | None = None


# it will be set by build script
context: Context = None  # type: ignore


def patch(file: str | Path, line: int, code: str) -> None:
    with open(file, "r+") as fp:
        codes = fp.readlines()
        assert not code.count("\r") and not code.count("\n"), "no new line allowed in 'code'."
        assert line <= len(codes), "line is greater than the raw file has."
        codes[line - 1] = code.format(context.flag) + "\n"
        fp.seek(0)
        fp.writelines(codes)
