from pathlib import Path
from typing import Any


def generate_script(daemons: list[dict[str, Any]], dest: str | Path, entrypoint: list[str]) -> None:
    threads = "\n".join(
        f"Thread(target=run_daemon, kwargs={daemon!r}),"
        for daemon in daemons
    )

    content = (
        f"""
import os
import subprocess
from threading import Thread

def run_daemon(**kwargs):
    while True:
        subprocess.Popen(**kwargs).wait()

threads = [
{threads}
]

for thread in threads:
    thread.start()

subprocess.Popen({entrypoint!r}).communicate()

os._exit(0)  # force exit
        """
    ).strip() + "\n"

    with open(dest, "w") as fp:
        fp.write(content)
