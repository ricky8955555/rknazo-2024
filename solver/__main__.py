import os
import sys

from solver import flag as flagutils
from solver.context import challenge_count

SOLVED = "solved.txt"


def print_result(flags: list[str]) -> None:
    assert len(flags) == challenge_count, "incorrect amount of flags got."
    result = flagutils.decode_flags(flags)
    print("cheers! here is the code of Alipay red envelope.")
    print(f"恭喜你通过了所有的挑战! 下面是支付宝红包代码.")
    print(result.decode())


def check_flags(flags: list[str]) -> None:
    try:
        _ = list(map(flagutils.extract_flag_data, flags))
    except AssertionError:
        raise
    except Exception as ex:
        assert False, f"decoding failed: {ex}"
    assert len(set(map(flagutils.extract_index, flags))) == len(flags), "duplicate index found."


def load_solved() -> list[str]:
    if not os.path.exists(SOLVED):
        return []
    with open(SOLVED, "r") as fp:
        return fp.read().splitlines()


def save_solved(flags: list[str]) -> None:
    with open(SOLVED, "w") as fp:
        fp.write("\n".join(flags))


def main() -> None:
    flags = load_solved()
    check_flags(flags)

    if len(flags) == challenge_count:
        return print_result(flags)

    flag = input("please type your flag (请输入 flag): ")
    flags.append(flag)
    check_flags(flags)
    save_solved(flags)

    seq = flagutils.extract_index(flag) + 1
    print(f"you've successfully solved challenge {seq}!")
    print(f"恭喜你通过第 {seq} 个挑战!")

    if len(flags) == challenge_count:
        return print_result(flags)

    print(f"{len(flags)} challenges solved, {challenge_count - len(flags)} left.")
    print(f"已解决 {len(flags)}, 剩余 {challenge_count - len(flags)}.")


try:
    main()
except AssertionError as ex:
    exit(print("err:", ex, file=sys.stderr))
