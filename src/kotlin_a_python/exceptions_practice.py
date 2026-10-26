def to_int_or_none(text: str) -> int | None:
    try:
        return int(text)
    except ValueError:
        return None


class InvalidWorkoutError(Exception):
    pass


def validate_duration(minutes: int) -> int:
    if 1 <= minutes <= 300:
        return minutes
    else:
        raise InvalidWorkoutError(f"Duration must be between 1 and 300, got {minutes}")


def parse_workout_line(line: str) -> tuple[str, int]:
    try:
        name, raw_duration = line.split(",")
        duration = int(raw_duration)
    except ValueError as e:
        raise InvalidWorkoutError(f"Bad line: {line}") from e
    return name, validate_duration(duration)


def main() -> None:
    print(to_int_or_none("42"))
    print(to_int_or_none("abc"))
    print()

    lines = ["Bench press,45", "Squat,abc", "Row", "Curl,0", "Deadlift,60"]
    for line in lines:
        try:
            name, minutes = parse_workout_line(line)
        except InvalidWorkoutError as e:
            print(f"Skipped: {e}")
        else:
            print(f"OK: {name} - {minutes} min")


if __name__ == "__main__":
    main()
