import os
import subprocess

from build import buildinfo


def build():
    buildinfo.patch("src/challenge.c", 76, 'flag = AY_OBFUSCATE("{}");')
    subprocess.run(["g++", "src/challenge.c", "-o", "challenge", "-O2"]).check_returncode()


def post():
    os.chmod("challenge", 0o700)


metadata = buildinfo.Metadata(
    name="perm",
    artifact="challenge",
    build=build,
    post=post,
)
