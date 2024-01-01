import os
import subprocess

from build import buildinfo


def build():
    buildinfo.patch("src/challenge.c", 4, 'const char flag[] = "{}";')
    subprocess.run(["gcc", "src/challenge.c", "-o", "challenge", "-O2"]).check_returncode()


def post():
    os.chmod("challenge", 0o700)


metadata = buildinfo.Metadata(
    name="binary",
    artifact="challenge",
    build=build,
    post=post,
)
