import parse


def part_1():
    success_counter = 0
    with open("inputs/day_2.txt", "r") as file:
        for item in file.readlines():
            item = item.split("\n")[0]
            result = parse.parse("{min:d}-{max:d} {letter}: {password}", item)

            if (
                result["min"]
                <= result["password"].count(result["letter"])
                <= result["max"]
            ):
                success_counter += 1
    return success_counter


def part_2():
    success_counter = 0
    with open("inputs/day_2.txt", "r") as file:
        for item in file.readlines():
            item = item.split("\n")[0]
            result = parse.parse("{pos_1:d}-{pos_2:d} {letter}: {password}", item)

            pos_1 = result["pos_1"] - 1
            pos_2 = result["pos_2"] - 1

            if (result["password"][pos_1] == result["letter"]) ^ (
                result["password"][pos_2] == result["letter"]
            ):
                success_counter += 1
    return success_counter


if __name__ == "__main__":
    print(part_2())
