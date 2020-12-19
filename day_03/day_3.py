def parse_map(file):
    three_map = []
    for line in file.read().splitlines():
        three_map += [[]]
        for item in line:
            three_map[-1] += [item == "#"]

    line_len = len(three_map[0])
    assert all([len(line) == line_len for line in three_map])
    return three_map


def parse_map(file):
    three_map = []
    for line_index, item in (
        (line_index, item)
        for line_index, line in enumerate(file.read().splitlines())
        for item in line
    ):
        if len(three_map) < line_index + 1:
            three_map += [[]]
        three_map[line_index] += [item == "#"]

    line_len = len(three_map[0])
    assert all([len(line) == line_len for line in three_map])
    return three_map


def print_map(three_map):
    for line in three_map:
        for item in line:
            print("#" if item else ".", end="")
        print()


def part_1(delta_col, delta_line):
    with open("inputs/day_3_sample.txt", "r") as file:
        three_map = parse_map(file)
    num_rows = len(three_map)
    num_cols = len(three_map[0])

    line_index = 0
    col_index = 0

    three_counter = 0

    while line_index < num_rows:
        if three_map[line_index][col_index]:
            three_counter += 1
        line_index += delta_line
        col_index = (col_index + delta_col) % num_cols
    return three_counter


def part_2():
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    acc = 1
    for slope in slopes:
        threes = part_1(*slope)
        print(f"Slope {slope}: {threes}")
        acc *= threes
    return acc


if __name__ == "__main__":
    print(part_1(delta_line=1, delta_col=3))
    print(part_2())
