import contextlib
import importlib
import os
import shutil

from pathlib import Path
from tempfile import TemporaryDirectory

from build import buildinfo
from build.buildinfo import Context, Metadata


working_dir = Path(os.getcwd())


def get_metadata(path: str | Path) -> Metadata:
    path = Path(path)
    buildinfo_path = path / "buildinfo.py"
    assert buildinfo_path.exists(), f"'buildinfo.py' was not found in '{path}'."
    try:
        if buildinfo_path.is_absolute():
            buildinfo_path = buildinfo_path.relative_to(working_dir)
    except ValueError:
        assert False, f"unable to import '{buildinfo_path}'."
    info = importlib.import_module(buildinfo_path.with_suffix("").as_posix().replace("/", "."))
    assert isinstance(
        metadata := getattr(info, "metadata", None), Metadata
    ), f"unable to get metadata from '{info}'."
    return metadata


def build(
    context: Context,
    path: str | Path,
    target: str | Path,
) -> None:
    metadata = get_metadata(path)

    target = Path(target)
    assert not target.exists(), "target directory should not exists."

    try:
        with TemporaryDirectory() as tmpdir:
            shutil.copytree(path, tmpdir, dirs_exist_ok=True)
            buildinfo.context = context
            os.chdir(tmpdir)
            metadata.build()
            artifact = Path(metadata.artifact)
            assert artifact.exists(), "artifact does not exists."
            if artifact.is_file():
                os.makedirs(target, exist_ok=True)
                shutil.copy(artifact, target)
            else:
                shutil.copytree(artifact, target)
        if metadata.post:
            os.chdir(target)
            metadata.post()
    except Exception:
        with contextlib.suppress(Exception):
            shutil.rmtree(target)
        raise
    finally:
        buildinfo.context = None
        os.chdir(working_dir)
