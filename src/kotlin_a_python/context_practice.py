import time
from collections.abc import Generator
from contextlib import contextmanager


def write_lines(path: str, lines: list[str]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(f"{line}\n" for line in lines)


def read_lines(path: str) -> list[str]:
    with open(path, encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


@contextmanager
def timer(label: str) -> Generator[None]:
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label} took {elapsed:.2f}s")


def main() -> None:
    path = "workouts.txt"
    write_lines(path, ["Bench press,45", "Squat,50", "Row,40"])

    with timer("Reading"):
        lines = read_lines(path)
        time.sleep(0.5)  # simulate slow work
    print(lines)

    try:
        with timer("Failing"):
            raise ValueError("boom")
    except ValueError as e:
        print(f"Caught: {e}")


if __name__ == "__main__":
    main()
