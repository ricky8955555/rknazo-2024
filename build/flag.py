import base64
from random import Random
import string


def generate_index_table(magic_bytes: bytes) -> bytes:
    random = Random(magic_bytes)
    index_table = list(string.ascii_letters)
    random.shuffle(index_table)
    return "".join(index_table).encode()


def generate_magic_num(magic_bytes: bytes) -> int:
    magic_num = int.from_bytes(magic_bytes)
    while magic_num > 255:
        magic_num >>= 1
    return magic_num


def generate_password(data: bytes) -> int:
    return pow(sum(data), abs(sum([data[0], *[~byte for byte in data[1:]]])), 255)


def generate_flags(result: bytes, magic_bytes: bytes) -> list[str]:
    assert len(result) % 2 == 0, "length of result should be divisible by 2."
    assert result.isascii(), "all chars of result should be ascii."

    index_table = generate_index_table(magic_bytes)
    challenge_count = len(result) // 2
    assert len(index_table) > 3, f"length of index table should be more than 3."
    assert (
        3 < challenge_count < len(index_table)
    ), f"challenge count should be more than 3 and less than {len(index_table)}."

    random = Random(magic_bytes)
    magic_num = generate_magic_num(magic_bytes)
    password = generate_password(result[:1] + magic_bytes + result[-1:])
    flags: list[str] = []

    for i in range(challenge_count):
        chars = result[i * 2 : i * 2 + 2]
        chars_int = int.from_bytes(chars) ^ magic_num
        if i not in [0, challenge_count - 1]:
            chars_int ^= password
        chars = chars_int.to_bytes(2)

        data = base64.b16encode(chars)
        assert len(data) == 4, "length of data should equals 4."

        raw_flag = "".join(random.choices(string.printable, k=16)).encode()
        raw_flag = (
            raw_flag[: i % 4]
            + data
            + sum(chars).to_bytes(2)
            + raw_flag[(i % 4) + 6 : -2]
            + index_table[i].to_bytes()
            + index_table[~i].to_bytes()
        )

        flag = base64.b16encode(raw_flag).lower().decode()
        # make it uuid-like
        flag = "flag{{{}-{}-{}-{}-{}}}".format(
            flag[:8], flag[8:12], flag[12:16], flag[16:20], flag[20:]
        )
        flags.append(flag)

    return flags


def validate_flags(result: bytes, flags: list[str], magic_bytes: bytes) -> None:
    index_table = generate_index_table(magic_bytes)
    magic_num = generate_magic_num(magic_bytes)
    results = [b""] * len(flags)

    for flag in flags:
        try:
            assert flag.index("flag{") == 0 and flag[-1:] == "}"
        except (ValueError, AssertionError):
            assert False, "flag should be wrapped in format 'flag{...}'"
        flag = flag.removeprefix("flag{").removesuffix("}")

        assert (
            list(map(len, flag.split("-", 5))) == [8, 4, 4, 4, 12]
        ), "format of flags should be 8-4-4-4-12"
        flag = base64.b16decode(flag.replace("-", "").upper())

        assert len(flag) == 16, "lengths of raw flags should be 16."

        assert (
            index_table[~(index := index_table.index(flag[-2]))] == flag[-1]
        ), "index validate failed."

        data = flag[index % 4 : (index % 4) + 4]
        chars = base64.b16decode(data)
        assert (
            sum(chars) == int.from_bytes(flag[(index % 4) + 4 : (index % 4) + 6])
        ), "check char sum failed."

        origin = (int.from_bytes(chars) ^ magic_num).to_bytes(2)
        results[index] = origin

    password = generate_password(
        results[0][:1] + magic_bytes + results[-1][-1:]
    )

    validating_result = b"".join((
        results[0],
        *((int.from_bytes(result) ^ password).to_bytes(2) for result in results[1:-1]),
        results[-1],
    ))

    assert (
        validating_result == result
    ), f"decoded result {validating_result} is not same as original one {result}."
