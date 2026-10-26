import asyncio
import time
from collections.abc import Generator
from contextlib import contextmanager

import httpx
from pydantic import BaseModel, Field

BASE_URL = "https://jsonplaceholder.typicode.com"


@contextmanager
def timer(label: str) -> Generator[None]:
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label} took {elapsed:.2f}s")


class User(BaseModel):
    id: int
    name: str
    email: str


class Post(BaseModel):
    id: int
    user_id: int = Field(alias="userId")
    title: str


async def fetch_user(client: httpx.AsyncClient, user_id: int) -> User:
    response = await client.get(f"/users/{user_id}")
    response.raise_for_status()
    return User.model_validate(response.json())


async def fetch_posts_by_user(client: httpx.AsyncClient, user_id: int) -> list[Post]:
    response = await client.get("/posts", params={"userId": user_id})
    response.raise_for_status()
    return [Post.model_validate(post) for post in response.json()]


async def fetch_user_or_none(client: httpx.AsyncClient, user_id: int) -> User | None:
    try:
        return await fetch_user(client, user_id)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return None
        raise


async def main() -> None:
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        print("--- one user ---")
        user = await fetch_user(client, 1)
        print(user.name, user.email)

        print("\n--- users concurrently ---")
        with timer("users"):
            users = await asyncio.gather(*(fetch_user(client, i) for i in [1, 2, 3]))
        print([u.name for u in users])

        print("\n--- posts by user 1 ---")
        posts = await fetch_posts_by_user(client, 1)
        print(len(posts), posts[0].title)

        print("\n--- missing user ---")
        print(await fetch_user_or_none(client, 999))


if __name__ == "__main__":
    asyncio.run(main())
