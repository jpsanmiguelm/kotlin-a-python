from enum import Enum


class Weekday(Enum):
    MONDAY = "monday"
    WEDNESDAY = "wednesday"
    FRIDAY = "friday"


def main() -> None:
    by_name = Weekday["FRIDAY"]
    print(by_name.value)

    by_value = Weekday("monday")
    print(by_value.name)

    print([w.value for w in Weekday])

    api_day = "wednesday"
    day = Weekday(api_day)
    print(day == Weekday.WEDNESDAY)


if __name__ == "__main__":
    main()
