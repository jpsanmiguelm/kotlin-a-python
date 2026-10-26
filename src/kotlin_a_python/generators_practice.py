from collections.abc import Iterable, Iterator
from itertools import islice
from pathlib import Path


def countdown(n: int) -> Iterator[int]:
    while n > 0:
        yield n
        n -= 1


def fibonacci() -> Iterator[int]:
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def read_non_empty_lines(path: str) -> Iterator[str]:
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            yield line


def parse_minutes(lines: Iterable[str]) -> Iterator[int]:
    for line in lines:
        try:
            _, raw_minutes = line.split(",")
            minutes = int(raw_minutes)
        except ValueError:
            continue
        yield minutes


def main() -> None:
    print(list(countdown(3)))
    print(list(islice(fibonacci(), 8)))

    path = "minutes.txt"
    Path(path).write_text(
        "Bench press,45\n\nSquat,abc\nRow,40\nCurl,30\n", encoding="utf-8"
    )
    total = sum(parse_minutes(read_non_empty_lines(path)))
    print(total)


if __name__ == "__main__":
    main()
