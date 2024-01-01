import os

from build import buildinfo


def post():
    os.symlink(buildinfo.context.flag.encode().hex(), "flag.txt")


metadata = buildinfo.Metadata(
    name="shortcut",
    artifact="hint.txt",
    build=lambda: None,
    post=post,
)
