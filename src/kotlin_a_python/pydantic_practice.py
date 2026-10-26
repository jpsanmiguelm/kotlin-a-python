from dataclasses import dataclass
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError


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


class WorkoutDto(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: str
    title: str | None = None
    muscle: MuscleGroup
    duration_sec: int = Field(alias="durationSec", gt=0)
    completed_at: str | None = Field(alias="completedAt", default=None)

    def to_domain(self) -> Workout:
        return Workout(
            id=self.id,
            title=self.title if self.title is not None else "Untitled workout",
            muscle=self.muscle,
            duration_min=self.duration_sec // 60,
            is_completed=self.completed_at is not None,
        )


def main() -> None:
    raw_items: list[dict[str, Any]] = [
        {
            "id": "1",
            "title": "Push day",
            "muscle": "chest",
            "durationSec": 3600,
            "completedAt": "2026-10-20",
        },
        {"id": "2", "muscle": "legs", "durationSec": "2700"},
        {"id": "3", "title": "Pull day", "muscle": "back", "durationSec": -30},
        {"id": "4", "title": "Yoga", "muscle": "core", "durationSec": 1800},
        {"id": "5", "title": "Arms", "muscle": "arms"},
    ]

    for item in raw_items:
        try:
            dto = WorkoutDto.model_validate(item)
        except ValidationError as e:
            print(f"Invalid item {item['id']}: {e.errors()[0]['msg']}")
        else:
            w = dto.to_domain()
            print(w.title, w.muscle.name, w.duration_min, w.is_completed)

    print()
    dto = WorkoutDto.model_validate_json(
        '{"id": "9", "muscle": "back", "durationSec": 600}'
    )
    print(dto.model_dump_json())


if __name__ == "__main__":
    main()
