from build import buildinfo


def build():
    buildinfo.patch("src/.flag.txt", 1, "{}")


metadata = buildinfo.Metadata(
    name="hide_and_seek",
    artifact="src",
    build=build,
)
