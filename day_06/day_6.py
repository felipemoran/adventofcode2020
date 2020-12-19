def part_1(filename):
    with open(f"inputs/{filename}", "r") as file:
        lines = file.read().splitlines()

    sum = 0
    group_set = None
    for line in lines:
        if line == "":
            sum += len(group_set)
            group_set = None
            continue
        new_set = set([char for char in line])
        if group_set is None:
            group_set = new_set
            continue

        group_set = group_set.intersection(new_set)

    if group_set is not None:
        sum += len(group_set)

    return sum


# def part_1(filename):
#     with open(f"inputs/{filename}", "r") as file:
#         lines = file.read().splitlines()
#
#     sum = 0
#     group_sets = None
#     for line in lines:
#         if group_set is None:
#             group_sets = []
#         if line == "":
#             sum += len(group_set)
#             group_set = None
#             continue
#         group_set = group_set.union(set([char for char in line]))
#
#     if group_set is not None:
#         sum += len(group_set)
#
#     return sum


if __name__ == "__main__":
    assert part_1("day_6_sample.txt") == 6
    print(part_1("day_6.txt"))
