from typing import overload, List, Tuple

from multipledispatch import dispatch


@dispatch(str, int, int)
def byte(s, i, j) -> Tuple[int, ...]:
    i, j = i - 1, j - 1
    return tuple(ord(s[k]) for k in range(i, j + 1))


@dispatch(str)
def byte(s) -> int:
    """
    byte(s) -> int \n
    byte(s, i, j) -> Tuple[int, ...]
    """
    return ord(s[0])


if __name__ == '__main__':
    print(byte("abc"))
    print(byte("abc", 1, 3))
