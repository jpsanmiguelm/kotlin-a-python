from dataclasses import dataclass
from typing import assert_never


@dataclass(frozen=True)
class Loading:
    pass


@dataclass(frozen=True)
class Ok:
    data: list[str]


@dataclass(frozen=True)
class Fail:
    code: int
    message: str


@dataclass(frozen=True)
class Cancelled:
    pass


type ApiResult = Loading | Ok | Fail | Cancelled


def describe(result: ApiResult) -> str:
    match result:
        case Loading():
            return "Loading..."
        case Ok(data=l) if not l:
            return "No data"
        case Ok(data=l):
            return f"Got {len(l)} items"
        case Fail(code=401):
            return "Please log in again"
        case Fail(code=c) if c >= 500:
            return f"Server error ({c})"
        case Fail(code=c, message=m):
            return f"Error {c}: {m}"
        case Cancelled():
            return "Cancelled"
        case _:
            assert_never(result)


def main() -> None:
    results: list[ApiResult] = [
        Loading(),
        Ok(["bench", "squat", "row"]),
        Ok([]),
        Fail(401, "Unauthorized"),
        Fail(503, "Service unavailable"),
        Fail(404, "Not found"),
    ]
    for result in results:
        print(describe(result))


if __name__ == "__main__":
    main()
