import asyncio
from enum import Enum
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status
from pydantic import BaseModel, Field

EXERCISES = ["Bench press", "Squat", "Row"]


class MuscleGroup(Enum):
    CHEST = "chest"
    BACK = "back"
    LEGS = "legs"
    ARMS = "arms"


class WorkoutCreate(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    muscle: MuscleGroup
    duration_min: int = Field(gt=0, le=300)


class Workout(WorkoutCreate):
    id: int


class WorkoutUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=50)
    muscle: MuscleGroup | None = None
    duration_min: int | None = Field(default=None, gt=0, le=300)


SEED_WORKOUTS = [
    Workout(id=1, title="Push day", muscle=MuscleGroup.CHEST, duration_min=60),
    Workout(id=2, title="Leg day", muscle=MuscleGroup.LEGS, duration_min=45),
    Workout(id=3, title="Pull day", muscle=MuscleGroup.BACK, duration_min=50),
    Workout(id=4, title="Chest pump", muscle=MuscleGroup.CHEST, duration_min=30),
    Workout(id=5, title="Arms", muscle=MuscleGroup.ARMS, duration_min=25),
]


class WorkoutRepository:
    def __init__(self, workouts: list[Workout]) -> None:
        self._workouts = workouts

    def list_all(self) -> list[Workout]:
        return list(self._workouts)

    def get(self, workout_id: int) -> Workout | None:
        return next((w for w in self._workouts if w.id == workout_id), None)

    def title_exists(self, title: str, exclude_id: int | None = None) -> bool:
        return any(
            w.title.lower() == title.lower() and w.id != exclude_id
            for w in self._workouts
        )

    def add(self, data: WorkoutCreate) -> Workout:
        next_id = max((w.id for w in self._workouts), default=0) + 1
        new_workout = Workout(id=next_id, **data.model_dump())
        self._workouts.append(new_workout)
        return new_workout

    def replace(self, workout: Workout) -> None:
        for i, w in enumerate(self._workouts):
            if w.id == workout.id:
                self._workouts[i] = workout
                return

    def delete(self, workout_id: int) -> None:
        self._workouts = [w for w in self._workouts if w.id != workout_id]


@lru_cache
def get_repository() -> WorkoutRepository:
    return WorkoutRepository(list(SEED_WORKOUTS))


RepoDep = Annotated[WorkoutRepository, Depends(get_repository)]


def get_workout_or_404(workout_id: int, repo: RepoDep) -> Workout:
    workout = repo.get(workout_id)
    if workout is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workout {workout_id} not found",
        )
    return workout


WorkoutDep = Annotated[Workout, Depends(get_workout_or_404)]


def require_api_key(x_api_key: Annotated[str | None, Header()] = None) -> None:
    if x_api_key != "secret-123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key"
        )


app = FastAPI()


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Workout API is running"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/exercises")
async def exercises() -> list[str]:
    return EXERCISES


@app.get("/slow")
async def slow() -> dict[str, str]:
    await asyncio.sleep(1)
    return {"message": "done"}


@app.get("/workouts")
async def list_workouts(
    repo: RepoDep,
    muscle: MuscleGroup | None = None,
    min_duration: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
) -> list[Workout]:
    filtered_workouts = [w for w in repo.list_all() if w.duration_min >= min_duration]
    if muscle is not None:
        filtered_workouts = [w for w in filtered_workouts if muscle == w.muscle]

    return filtered_workouts[:limit]


@app.get("/workouts/summary")
async def workouts_summary(repo: RepoDep) -> dict[str, int]:
    workouts = repo.list_all()
    count = len(workouts)
    total_minutes = sum(w.duration_min for w in workouts)
    return {"count": count, "total_minutes": total_minutes}


@app.get("/workouts/{workout_id}")
async def get_workout(workout: WorkoutDep) -> Workout:
    return workout


@app.put("/workouts/{workout_id}", dependencies=[Depends(require_api_key)])
async def replace_workout(
    repo: RepoDep, workout: WorkoutDep, body: WorkoutCreate
) -> Workout:
    if repo.title_exists(body.title, workout.id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Workout '{body.title}' already exists",
        )
    replaced_workout = Workout(id=workout.id, **body.model_dump())
    repo.replace(replaced_workout)
    return replaced_workout


@app.patch("/workouts/{workout_id}", dependencies=[Depends(require_api_key)])
async def update_workout(
    repo: RepoDep, workout: WorkoutDep, body: WorkoutUpdate
) -> Workout:
    changes = body.model_dump(exclude_none=True, exclude_unset=True)
    if "title" in changes and repo.title_exists(changes["title"], workout.id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Workout '{body.title}' already exists",
        )
    updated = workout.model_copy(update=changes)
    repo.replace(updated)
    return updated


@app.delete(
    "/workouts/{workout_id}",
    dependencies=[Depends(require_api_key)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_workout(repo: RepoDep, workout: WorkoutDep) -> None:
    repo.delete(workout.id)


@app.post(
    "/workouts",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_api_key)],
)
async def create_workout(repo: RepoDep, body: WorkoutCreate) -> Workout:
    if repo.title_exists(body.title):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Workout '{body.title}' already exists",
        )
    new_workout = repo.add(body)
    return new_workout
