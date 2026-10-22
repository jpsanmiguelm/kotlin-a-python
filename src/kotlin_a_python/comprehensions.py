from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum

numbers = [3, 8, 1, 10, 5]
words = ["kotlin", "python", "dart"]

for n in numbers:
    print(n)

for i in range(3):
    print(i)

for i in range(1, 4):
    print(i)

for i in range(10, 0, -2):
    print(i)

for i, word in enumerate(words):
    print(i, word)

doubled = [n * 2 for n in numbers]
print(doubled)

big = [n for n in numbers if n > 4]
print(big)

big_doubled = [n * 2 for n in numbers if n > 4]
print(big_doubled)

labels = ["big" if n > 4 else "small" for n in numbers]
print(labels)

lenght = {w: len(w) for w in words}
print(lenght)

for word, length in lenght.items():
    print(word, length)

by_length = {len(w): w for w in words}
print(by_length)

for word, length in by_length.items():
    print(word, length)

upper = {w.upper(): len(w) for w in words}
print(upper)


for word, length in upper.items():
    print(word, length)

unique_lengths = {len(w) for w in words}
print(unique_lengths)
print(sorted(unique_lengths))

rows = [[1, 2], [2, 3], [3, 4], [4, 5]]

flat = [x for row in rows for x in row]
print(flat)


flatSet = {x for row in rows for x in row}
print(flatSet)

as_list = [n * 2 for n in numbers]
print(as_list)
as_gen = (n * 2 for n in numbers)
print(as_gen)

sum2 = sum(n * 2 for n in numbers)
print(sum2)
any2 = any(n > 9 for n in numbers)
print(any2)
all = all(n > 0 for n in numbers)
print(all)
max2 = max(n * 2 for n in numbers)
print(max)
join = ", ".join(w.upper() for w in words)
print(join)

gen = (n * 2 for n in numbers)
print(sum(gen))
print(sum(gen))

maxWords = max(words, key=lambda w: len(w))
print(maxWords)

maxWords2 = max(words, key=len)
print(maxWords2)

maxWordsAlph = max(words)
print(maxWordsAlph)

minWords = min(words, key=lambda w: len(w))
print(minWords)

minWords2 = min(words, key=len)
print(minWords2)

minWordsAlph = min(words)
print(minWordsAlph)

sortedLen = sorted(words, key=len)
print(sortedLen)

sortedLenReverse = sorted(words, key=len, reverse=True)
print(sortedLenReverse)

srotedNum = sorted(numbers)
print(srotedNum)

sortedNumReverse = sorted(numbers, reverse=True)
print(sortedNumReverse)

sortedTuple = sorted(words, key=lambda w: (len(w), w))
print(sortedTuple)

maxNull = max([], key=len, default=None)
print(maxNull)

longest = max(words, key=len)
print(longest)
longest_upper = max(words, key=len).upper()
print(longest_upper)

groups: dict[int, list[str]] = {}
for w in words:
    key = len(w)
    if key not in groups:
        groups[key] = []
    groups[key].append(w)

print(groups)

by_length_dict: defaultdict[int, list[str]] = defaultdict(list)
for w in words:
    by_length_dict[len(w)].append(w)

print(dict(by_length_dict))


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


exercises = [
    Exercise("Bench press", 4, 8, 60.0, muscles=["chest", "triceps"]),
    Exercise("Squat", 5, 5, 80.0, muscles=["quads", "glutes"]),
    Exercise("Bicep curl", 3, 12, 12.0, muscles=["biceps"]),
    Exercise("Barbell row", 4, 10, 55.0, muscles=["back", "biceps"]),
]

heavy_names = [e.name for e in exercises if e.weight_kg > 50]
print(heavy_names)

volume_by_name = {e.name: e.volume() for e in exercises}
print(volume_by_name)

total_sets = sum(e.sets for e in exercises)
print(total_sets)

all_muscles = sorted({m for e in exercises for m in e.muscles})
print(all_muscles)

has_very_heavy = any(e.weight_kg > 75 for e in exercises)
print(has_very_heavy)

top_by_volume = max(exercises, key=lambda e: e.volume()).name
print(top_by_volume)

names_by_volume_desc = [
    e.name for e in sorted(exercises, key=lambda e: e.volume(), reverse=True)
]
print(names_by_volume_desc)


class MuscleGroup(Enum):
    CHEST = "chest"
    BACK = "back"
    LEGS = "legs"


m = MuscleGroup.CHEST

print(m.name)
print(m.value)
print(m == MuscleGroup.CHEST)
print(m)

for m in MuscleGroup:
    print(m)

print([m for m in MuscleGroup])
