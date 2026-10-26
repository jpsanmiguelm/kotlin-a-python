import asyncio
import time
from collections.abc import Generator
from contextlib import contextmanager


@contextmanager
def timer(label: str) -> Generator[None]:
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label} took {elapsed:.2f}s")


async def fetch_or_fail(workout_id: str, delay_sec: float, fail: bool = False) -> str:
    print(f"Fetching {workout_id}...")
    try:
        await asyncio.sleep(delay_sec)
    except asyncio.CancelledError:
        print(f"Cancelled {workout_id}")
        raise  # always re-raise (3.2)
    if fail:
        raise ValueError(f"Workout {workout_id} not found")
    return f"workout-{workout_id}"


async def fetch_with_timeout(
    workout_id: str, delay_sec: float, timeout: float
) -> str | None:
    try:
        async with asyncio.timeout(timeout):
            return await fetch_or_fail(workout_id, delay_sec)
    except TimeoutError:
        return None


async def fetch_all_tolerant(delays: dict[str, float], failing: set[str]) -> list[str]:
    results = await asyncio.gather(
        *(fetch_or_fail(wid, delay, wid in failing) for wid, delay in delays.items()),
        return_exceptions=True,
    )
    successes: list[str] = []
    for r in results:
        if isinstance(r, BaseException):
            print(f"Failed: {r}")
        else:
            successes.append(r)

    return successes


async def fetch_all_strict(delays: dict[str, float], failing: set[str]) -> list[str]:
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(fetch_or_fail(wid, delay, wid in failing))
            for wid, delay in delays.items()
        ]
    return [task.result() for task in tasks]


async def main() -> None:
    print("--- timeout ---")
    print(await fetch_with_timeout("fast", 0.2, timeout=0.5))
    print(await fetch_with_timeout("slow", 2.0, timeout=0.5))

    delays = {"a": 0.2, "b": 1.0, "c": 0.5}

    print("\n--- tolerant ---")
    with timer("tolerant"):
        results = await fetch_all_tolerant(delays, failing={"a"})
    print(results)

    print("\n--- strict ---")
    with timer("strict"):
        try:
            await fetch_all_strict(delays, failing={"a"})
        except* ValueError as eg:
            print(f"Group failed: {[str(e) for e in eg.exceptions]}")


if __name__ == "__main__":
    asyncio.run(main())
