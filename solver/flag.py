import base64

from solver.context import index_table, magic_bytes


def _get_magic_num() -> int:
    magic_num = int.from_bytes(magic_bytes)
    while magic_num > 255:
        magic_num >>= 1
    return magic_num


def _unwrap_flag(flag: str) -> str:
    try:
        assert flag.index("flag{") == 0 and flag[-1] == "}", "invalid flag format."
    except ValueError:
        assert False, "invalid flag format."
    return flag[5:-1]


def _get_raw_flag(flag: str) -> bytes:
    # fmt: off
    flag = _unwrap_flag(flag)
    assert (
        list(map(len, flag.split("-", 5))) == [8, 4, 4, 4, 12]
    ), "invalid flag format."
    # fmt: on
    flag = flag.replace("-", "")
    raw_flag = base64.b16decode(flag.upper())
    assert len(raw_flag) == 16, "invalid flag got."
    return raw_flag


def _generate_password(data: bytes) -> int:
    return pow(sum(data), abs(sum([data[0], *[~byte for byte in data[1:]]])), 255)


def extract_index(flag: str) -> int:
    raw_flag = _get_raw_flag(flag)
    try:
        assert index_table[~(index := index_table.index(raw_flag[-2]))] == raw_flag[-1]
    except ValueError:
        assert False, "index validate failed."
    return index


def extract_flag_data(flag: str) -> bytes:
    index = extract_index(flag)
    raw_flag = _get_raw_flag(flag)
    magic = raw_flag[index % 4 : (index % 4) + 4]
    chars = base64.b16decode(magic)
    assert sum(chars) == int.from_bytes(
        raw_flag[(index % 4) + 4 : (index % 4) + 6]
    ), "checksum failed."
    magic_num = _get_magic_num()
    return int.to_bytes(int.from_bytes(chars) ^ magic_num, 2)


def decode_flags(flags: list[str]) -> bytes:
    flags = sorted(flags, key=lambda flag: extract_index(flag))
    results = list(map(extract_flag_data, flags))
    password = _generate_password(results[0][:1] + magic_bytes + results[-1][-1:])
    result = b"".join(
        (
            results[0],
            *((int.from_bytes(result) ^ password).to_bytes(2) for result in results[1:-1]),
            results[-1],
        )
    )
    return result
