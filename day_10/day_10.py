from collections import defaultdict


def number_of_paths(curr_index, numbers, distances):
    acc = 0
    if curr_index == len(numbers) - 1:
        distances[curr_index] = 1
        return 1

    curr_number = numbers[curr_index]
    for next_index, next_number in enumerate(numbers[curr_index + 1 :], curr_index + 1):
        if next_number - curr_number > 3:
            break
        if next_index not in distances:
            distances[next_index] = number_of_paths(next_index, numbers, distances)
        acc += distances[next_index]
    return acc


def part_2(filename):
    with open(f"inputs/{filename}", "r") as file:
        numbers = [int(line) for line in file.read().splitlines()]

    numbers += [max(numbers) + 3, 0]
    numbers.sort()
    distances = {}

    total = number_of_paths(0, numbers, distances)
    return total


def part_1(filename):
    with open(f"inputs/{filename}", "r") as file:
        numbers = [int(line) for line in file.read().splitlines()]

    numbers += [max(numbers) + 3, 0]
    numbers.sort()

    gaps = defaultdict(lambda: 0, {})
    for a, b in zip(numbers[:-1], numbers[1:]):
        gaps[b - a] += 1

    return gaps[1] * gaps[3]


if __name__ == "__main__":
    print(part_1("day_10_sample.txt"))
    print(part_1("day_10_sample_2.txt"))
    print(part_1("day_10.txt"))

    print(part_2("day_10_sample.txt"))
    print(part_2("day_10_sample_2.txt"))
    print(part_2("day_10.txt"))
