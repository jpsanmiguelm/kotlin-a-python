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


def slow_sync_fetch(workout_id: str, delay_sec: float) -> str:
    """A sync function, like an old library or a sync SDK client."""
    print(f"Fetching {workout_id}...")
    time.sleep(delay_sec)
    return f"workout-{workout_id}"


async def heartbeat() -> None:
    """Prints 'tick' every 0.25s while the event loop is free."""
    while True:
        print("  tick")
        await asyncio.sleep(0.25)


async def bad_fetch(workout_id: str, delay_sec: float) -> str:
    return slow_sync_fetch(workout_id, delay_sec)  # ❌ blocks the event loop


async def good_fetch(workout_id: str, delay_sec: float) -> str:
    return await asyncio.to_thread(slow_sync_fetch, workout_id, delay_sec)


async def main() -> None:
    print("--- blocking ---")
    beat = asyncio.create_task(heartbeat())
    with timer("blocking"):
        results = await asyncio.gather(bad_fetch("1", 1.0), bad_fetch("2", 1.0))
    beat.cancel()
    print(results)

    print("\n--- to_thread ---")
    beat = asyncio.create_task(heartbeat())
    with timer("to_thread"):
        results = await asyncio.gather(good_fetch("1", 1.0), good_fetch("2", 1.0))
    beat.cancel()
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
