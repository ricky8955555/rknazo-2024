from pathlib import Path
from build import flag as flagutils


def generate_solver_context(magic_bytes: bytes, challenge_count: int, path: str | Path) -> None:
    content = (
        f"""
index_table = {flagutils.generate_index_table(magic_bytes)!r}
magic_bytes = {magic_bytes!r}
challenge_count = {challenge_count!r}
        """
    ).strip() + "\n"

    with open(path, "w") as fp:
        fp.write(content)


def validate_flags(result: bytes, flags: list[str], magic_bytes: bytes) -> None:
    import solver.context
    solver.context.index_table = flagutils.generate_index_table(magic_bytes)
    solver.context.challenge_count = len(flags)
    solver.context.magic_bytes = magic_bytes

    import solver.flag
    assert solver.flag.decode_flags(flags) == result, "validate result failed in solver."
