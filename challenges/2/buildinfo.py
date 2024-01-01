import base64

from build import buildinfo


def build():
    # fmt: off
    buildinfo.patch(
        "flag.txt", 1,
        base64.b64encode(base64.b64encode(buildinfo.context.flag.encode())).decode(),
    )
    # fmt: on


metadata = buildinfo.Metadata(
    name="easy_encoding",
    artifact="flag.txt",
    build=build,
)
