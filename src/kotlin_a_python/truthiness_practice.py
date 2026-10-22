def describe_list(items: list[str]) -> str:
    if not items:
        return "empty"
    return f"{len(items)} items"


def display_name(name: str | None) -> str:
    return name or "Anonymous"


def is_blank(text: str | None) -> bool:
    return not text or not text.strip()


def reps_label(reps: int | None) -> str:
    if reps is None:
        return "not set"
    return f"{reps} reps"


def main() -> None:
    print(describe_list([]))
    print(describe_list(["bench", "squat"]))

    print(display_name(None))
    print(display_name(""))
    print(display_name("Juan"))

    print(is_blank(None))
    print(is_blank("   "))
    print(is_blank("hi"))

    print(reps_label(None))
    print(reps_label(0))
    print(reps_label(8))


if __name__ == "__main__":
    main()
