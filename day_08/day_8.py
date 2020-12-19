import copy


def execute(operation, argument, state):
    if operation == "nop":
        state["pc"] += 1
    elif operation == "acc":
        state["pc"] += 1
        state["acc"] += argument
    elif operation == "jmp":
        state["pc"] += argument


def part_1(filename):
    with open(f"inputs/{filename}", "r") as file:
        lines = file.read().splitlines()

    instructions = [
        {
            "operation": line.split(" ")[0],
            "argument": int(line.split(" ")[1]),
            "is_used": False,
        }
        for line in lines
    ]

    state = {"pc": 0, "acc": 0}
    run(instructions, state)

    return state["acc"]


def part_2(filename):
    with open(f"inputs/{filename}", "r") as file:
        lines = file.read().splitlines()

    instructions = [
        {
            "operation": line.split(" ")[0],
            "argument": int(line.split(" ")[1]),
            "is_used": False,
        }
        for line in lines
    ]

    for index, instruction in enumerate(instructions):
        if instruction["operation"] == "acc":
            continue
        new_instructions = copy.deepcopy(instructions)
        new_instructions[index]["operation"] = (
            "nop" if instruction["operation"] == "jmp" else "jmp"
        )

        state = {"pc": 0, "acc": 0}
        is_infinite_loop = run(new_instructions, state)

        if not is_infinite_loop:
            return state["acc"]


def run(instructions, state):
    is_infinite_loop = False
    while True:
        if state["pc"] == len(instructions):
            break
        if instructions[state["pc"]]["is_used"]:
            is_infinite_loop = True
            break
        instructions[state["pc"]]["is_used"] = True
        execute(
            instructions[state["pc"]]["operation"],
            instructions[state["pc"]]["argument"],
            state,
        )
    return is_infinite_loop


if __name__ == "__main__":
    print(part_1("day_8_sample.txt"))
    print(part_1("day_8.txt"))
    print(part_2("day_8.txt"))
