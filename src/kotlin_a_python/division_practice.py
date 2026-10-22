def to_minutes(seconds: int) -> int:
    return seconds // 60


print(to_minutes(2750))


def format_duration(seconds: int) -> str:
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    return f"{hours}h {minutes}m {secs}s"


print(format_duration(3725))


def average_miutes(durations_sec: list[int]) -> float:
    sum_secs = sum(durations_sec)
    total_secs = len(durations_sec)
    minutes = (sum_secs / total_secs) / 60
    return round(minutes, 1)


print(average_miutes([3600, 2700, 3000]))
