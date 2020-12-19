from itertools import product


def part_1(filename, preamble_size):
    with open(f"inputs/{filename}", "r") as file:
        numbers = [int(line) for line in file.read().splitlines()]

    for index, item in enumerate(numbers):
        if index < preamble_size:
            continue

        for a, b in product(
            numbers[index - preamble_size : index],
            numbers[index - preamble_size : index],
        ):
            if a == b:
                continue
            if a + b == item:
                break
        else:
            return item
    return None


def part_2(filename, weak_number):
    with open(f"inputs/{filename}", "r") as file:
        numbers = [int(line) for line in file.read().splitlines()]

    for i in range(2, len(numbers)):
        for j in range(0, len(numbers) - i):
            lookup_range = numbers[j : j + i]
            if sum(lookup_range) != weak_number:
                continue
            return min(lookup_range) + max(lookup_range)


if __name__ == "__main__":
    print(part_1("day_9_sample.txt", 5))
    weak_number = part_1("day_9.txt", 25)
    print(part_2("day_9.txt", weak_number))
