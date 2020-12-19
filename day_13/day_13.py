import math
from functools import reduce


def part_1(filename):
    with open(f"inputs/{filename}", "r") as file:
        earliest_timestamp = int(file.readline())
        busses = [int(item) for item in file.readline().split(",") if item != "x"]

    earliest_departures = [
        (math.ceil(earliest_timestamp / bus) * bus, bus) for bus in busses
    ]

    earliest_departure = reduce(
        lambda earliest, item: item if item[0] < earliest[0] else earliest,
        earliest_departures,
    )
    return (earliest_departure[0] - earliest_timestamp) * earliest_departure[1]


def calculate_n(b1, i1, b2, i2, n2):
    return (b2 * n2 - i2 + i1) / b1


def is_good_single(b1, i1, b2, i2, n2):
    n1 = calculate_n(b1, i1, b2, i2, n2)
    return n1 == round(n1)


def calculate_t(b, i, n):
    return b * n - i


def part_2(filename):
    with open(f"inputs/{filename}", "r") as file:
        earliest_timestamp = int(file.readline())
        busses = [
            (bus_index, int(bus_frequency))
            for bus_index, bus_frequency in enumerate(file.readline().split(","))
            if bus_frequency != "x"
        ]

    multipliers = [
        reduce(
            lambda multiplier, bus: multiplier
            if bus[0] == index
            else multiplier * bus[1][1],
            enumerate(busses),
            1,
        )
        for index, bus in enumerate(busses)
    ]

    total = 0
    for (bus_index, bus_frequency), multiplier in zip(busses, multipliers):
        n = None
        remainder = None
        while remainder != (-bus_index) % bus_frequency:
            if n is None:
                n = 0
            else:
                n += 1
            remainder = (n * multiplier) % bus_frequency
        total += multiplier * n
    total = total % reduce(lambda a, b: a * b[1], busses, 1)
    return total


if __name__ == "__main__":
    # res = part_1("day_13_sample_1.txt")
    # assert res == 295
    #
    # print(part_1("day_13.txt"))
    for i in range(1, 7):
        print(i, part_2(f"day_13_sample_{i}.txt"))
    print(part_2("day_13.txt"))
