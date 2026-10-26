import asyncio
import time
from collections.abc import Generator
from contextlib import contextmanager


async def fetch_workout(workout_id: str, delay_sec: float) -> str:
    print(f"Fetching {workout_id}...")
    await asyncio.sleep(delay_sec)
    return f"workout-{workout_id}"


@contextmanager
def timer(label: str) -> Generator[None]:
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label} took {elapsed:.2f}s")


async def fetch_pair() -> tuple[str, str]:
    first, second = await asyncio.gather(
        fetch_workout("1", 1.0), fetch_workout("2", 1.0)
    )
    return first, second


async def fetch_many_gather(delays: dict[str, float]) -> list[str]:
    coroutines = [
        fetch_workout(workout_id, delay) for workout_id, delay in delays.items()
    ]
    return await asyncio.gather(*coroutines)


async def fetch_many_taskgroup(delays: dict[str, float]) -> list[str]:
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(fetch_workout(workout_id, delay))
            for workout_id, delay in delays.items()
        ]
    return [task.result() for task in tasks]


async def fetch_many_limited(delays: dict[str, float], limit: int) -> list[str]:
    sem = asyncio.Semaphore(limit)

    async def limited_fetch_workout(workout_id: str, delay: float) -> str:
        async with sem:
            return await fetch_workout(workout_id, delay)

    return await asyncio.gather(
        *(
            limited_fetch_workout(workout_id, delay)
            for workout_id, delay in delays.items()
        )
    )


async def main() -> None:
    print("--- pair ---")
    with timer("pair"):
        first, second = await fetch_pair()
    print(f"Fetched {first} and {second}")

    delays = {"a": 0.3, "b": 1.0, "c": 0.5, "d": 0.2, "e": 0.8}

    print("\n--- gather ---")
    with timer("gather"):
        results = await fetch_many_gather(delays)
    print(results)

    print("\n--- taskgroup ---")
    with timer("taskgroup"):
        results = await fetch_many_taskgroup(delays)
    print(results)

    print("\n--- limited ---")
    with timer("limited"):
        results = await fetch_many_limited(
            {"w1": 1.0, "w2": 1.0, "w3": 1.0, "w4": 1.0}, limit=2
        )
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
