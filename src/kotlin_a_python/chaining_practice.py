def top_words(words: list[str]) -> list[str]:
    return sorted({w.lower() for w in words if len(w) > 3})[:3]


def passing_labels(scores: dict[str, int]) -> list[str]:
    passing = {name: score for name, score in scores.items() if score >= 60}
    ranked = sorted(passing.items(), key=lambda item: item[1], reverse=True)
    return [f"{name}: {score}" for name, score in ranked]


def slugify(text: str) -> str:
    return text.strip().lower().replace(" ", "-")


def cheap_products(prices: dict[str, float]) -> list[str]:
    filtered = {name: price for name, price in prices.items() if price < 50}
    ordered = sorted(filtered.items(), key=lambda item: item[1])
    return [f"{name} costs ${price}" for name, price in ordered]


def top_muscles(minutes_by_muscle: dict[str, int]) -> list[str]:
    filtered = {
        muscle: minutes
        for muscle, minutes in minutes_by_muscle.items()
        if minutes >= 25
    }
    sorted_muscles = sorted(filtered.items(), key=lambda item: item[1], reverse=True)[
        :3
    ]
    return [f"{muscle.upper()} - {minutes} min" for muscle, minutes in sorted_muscles]


def main() -> None:
    words = ["Python", "kotlin", "AI", "Dart", "python", "Rust", "go", "Swift"]
    print(top_words(words))

    scores = {"Ana": 82, "Luis": 45, "Juan": 91, "Sara": 60, "Leo": 58}
    print(passing_labels(scores))

    print(slugify("  Hello AI World  "))


# if __name__ == "__main__":
#     main()


def main2() -> None:
    prices = {
        "Protein": 49.99,
        "Creatine": 25.0,
        "Shaker": 8.5,
        "Rack": 120.0,
        "Bands": 15.0,
        "Bench": 89.9,
    }
    print(cheap_products(prices))

    minutes_by_muscle = {"chest": 90, "back": 50, "legs": 90, "arms": 25, "core": 10}
    print(top_muscles(minutes_by_muscle))


if __name__ == "__main__":
    main2()
