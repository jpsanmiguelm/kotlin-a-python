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
any = any(n > 9 for n in numbers)
print(any)
all = all(n > 0 for n in numbers)
print(all)
max = max(n * 2 for n in numbers)
print(max)
join = ", ".join(w.upper() for w in words)
print(join)

gen = (n * 2 for n in numbers)
print(sum(gen))
print(sum(gen))
