import os
import subprocess

from build import buildinfo


def build():
    os.chdir("daemon")
    buildinfo.patch("src/main.rs", 17, 'static FLAG: Lazy<String> = Lazy::new(|| lc!("{}"));')
    subprocess.run(["cargo", "build", "--release"]).check_returncode()
    os.chdir("../")
    os.rename("daemon/target/release/daemon", "out/.daemon")


def post():
    os.chmod(".daemon", 0o700)
    buildinfo.context.make_daemon(["./.daemon"])


metadata = buildinfo.Metadata(
    name="site",
    artifact="out",
    build=build,
    post=post,
)
