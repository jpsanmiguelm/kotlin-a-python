from dataclasses import dataclass
from enum import Enum
from typing import assert_never


class MuscleGroup(Enum):
    CHEST = "chest"
    BACK = "back"
    LEGS = "legs"
    ARMS = "arms"


@dataclass(frozen=True)
class Workout:
    id: str
    title: str
    muscle: MuscleGroup
    duration_min: int
    is_completed: bool


@dataclass(frozen=True)
class WorkoutDto:
    id: str
    title: str | None
    muscle: str
    duration_sec: int
    completed_at: str | None

    def to_domain(self) -> Workout:
        return Workout(
            id=self.id,
            title=self.title if self.title is not None else "Untitled workout",
            muscle=MuscleGroup[self.muscle.upper()],
            duration_min=self.duration_sec // 60,
            is_completed=self.completed_at is not None,
        )


@dataclass(frozen=True)
class Loading:
    pass


@dataclass(frozen=True)
class Success:
    workouts: list[Workout]


@dataclass(frozen=True)
class Error:
    message: str
    can_retry: bool = True


type WorkoutUiState = Loading | Success | Error


def to_screen_text(state: WorkoutUiState) -> str:
    match state:
        case Loading():
            return "Loading..."
        case Success(workouts=w) if not w:
            return "No workouts yet"
        case Success(workouts=w):
            return f"{len(w)} workouts"
        case Error(message=m, can_retry=True):
            return f"Error: {m}. Tap to retry"
        case Error(message=m):
            return f"Error: {m}"
        case _:
            assert_never(state)


def main() -> None:
    dtos = [
        WorkoutDto("1", "Push day", "chest", 3600, "2026-10-20"),
        WorkoutDto("2", None, "legs", 2700, "2026-10-19"),
        WorkoutDto("3", "Pull day", "back", 3000, None),
        WorkoutDto("4", "Chest pump", "chest", 1800, "2026-10-21"),
        WorkoutDto("5", "Arms", "arms", 1500, "2026-10-18"),
    ]

    # Snippet 1
    workouts = [dto.to_domain() for dto in dtos]
    for w in workouts:
        print(w.title, w.muscle.name, w.duration_min, w.is_completed)
    print()

    # Snippet 2
    states: list[WorkoutUiState] = [
        Loading(),
        Success(workouts),
        Success([]),
        Error("Network down"),
        Error("Unauthorized", can_retry=False),
    ]
    for state in states:
        print(to_screen_text(state))


if __name__ == "__main__":
    main()
