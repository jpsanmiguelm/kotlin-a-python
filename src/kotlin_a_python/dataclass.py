from dataclasses import dataclass, field, replace


@dataclass(frozen=True)
class User:
    name: str
    age: int = 0
    nickname: str | None = None
    tags: list[str] = field(default_factory=list)

    def is_adult(self) -> bool:
        return self.age >= 18


first = User("Juan", 27, tags=["First, lol"])
second = User(name="Juan", age=27)

print(first)
print(second)
print(first == second)

older = replace(first, age=29, name="Sanmi")

print(older)

default = User("Sayan")

print(default.is_adult())


def main() -> None:
    print("hello")


if __name__ == "__main__":
    main()


@dataclass(frozen=True)
class Exercise:
    name: str
    sets: int
    reps: int
    weight_kg: float = 0.0
    notes: str | None = None
    muscles: list[str] = field(default_factory=list)

    def volume(self) -> float:
        return self.sets * self.reps * self.weight_kg


def my_main() -> None:
    bench = Exercise("Bench press", 4, 8, 60.0, muscles=["chest", "triceps"])
    print(bench)
    print(bench.volume())

    heavier = replace(bench, weight_kg=65.0)
    print(heavier)

    print(bench == Exercise("Bench press", 4, 8, 60.0, muscles=["chest", "triceps"]))


my_main()
