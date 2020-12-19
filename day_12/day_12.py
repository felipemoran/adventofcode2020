from enum import Enum


class Commands(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"
    LEFT = "L"
    RIGHT = "R"
    FORWARD = "F"


class Instruction:
    def __init__(self, instruction_str):
        self.command = Commands(instruction_str[0])
        self.value = int(instruction_str[1:])

    def __str__(self):
        return f"{self.command.value} {self.value}"


class Ship1:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = 90

    def execute(self, instruction):
        if instruction.command == Commands.NORTH:
            self.x += instruction.value
        elif instruction.command == Commands.SOUTH:
            self.x -= instruction.value
        elif instruction.command == Commands.EAST:
            self.y += instruction.value
        elif instruction.command == Commands.WEST:
            self.y -= instruction.value
        elif instruction.command == Commands.LEFT:
            if instruction.value % 90 != 0:
                raise ValueError
            self.direction = (self.direction - instruction.value) % 360
        elif instruction.command == Commands.RIGHT:
            if instruction.value % 90 != 0:
                raise ValueError
            self.direction = (self.direction + instruction.value) % 360
        elif instruction.command == Commands.FORWARD:
            if self.direction == 0:
                self.x += instruction.value
            elif self.direction == 90:
                self.y += instruction.value
            elif self.direction == 180:
                self.x -= instruction.value
            elif self.direction == 270:
                self.y -= instruction.value

    def manhattan_distance(self):
        return abs(self.x) + abs(self.y)


class Ship2:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = 90
        self.waypoint_x = 1
        self.waypoint_y = 10

    def execute(self, instruction):
        if instruction.command == Commands.NORTH:
            self.waypoint_x += instruction.value
        elif instruction.command == Commands.SOUTH:
            self.waypoint_x -= instruction.value
        elif instruction.command == Commands.EAST:
            self.waypoint_y += instruction.value
        elif instruction.command == Commands.WEST:
            self.waypoint_y -= instruction.value
        elif (
            instruction.command == Commands.LEFT
            or instruction.command == Commands.RIGHT
        ):
            if instruction.command == Commands.LEFT:
                value = -instruction.value
            else:
                value = instruction.value
            value = value % 360
            if value == 0:
                return
            elif value == 90:
                x = self.waypoint_x
                y = self.waypoint_y
                self.waypoint_x = -y
                self.waypoint_y = x
            elif value == 180:
                self.waypoint_x = -self.waypoint_x
                self.waypoint_y = -self.waypoint_y
            elif value == 270:
                x = self.waypoint_x
                y = self.waypoint_y
                self.waypoint_x = y
                self.waypoint_y = -x
        elif instruction.command == Commands.FORWARD:
            self.x += self.waypoint_x * instruction.value
            self.y += self.waypoint_y * instruction.value

    def manhattan_distance(self):
        return abs(self.x) + abs(self.y)


def part_1(filename):
    with open(filename, "r") as file:
        instructions = [Instruction(line) for line in file.readlines()]

    ship = Ship1()
    for instruction in instructions:
        ship.execute(instruction)

    return ship.manhattan_distance()


def part_2(filename):
    with open(filename, "r") as file:
        instructions = [Instruction(line) for line in file.readlines()]

    ship = Ship2()
    print(ship.x, ship.y, ship.waypoint_x, ship.waypoint_y)
    for instruction in instructions:
        ship.execute(instruction)
        print(ship.x, ship.y, ship.waypoint_x, ship.waypoint_y)

    return ship.manhattan_distance()


if __name__ == "__main__":
    print(part_1("inputs/day_12_sample_1.txt"))
    print(part_1("inputs/day_12.txt"))

    print(part_2("inputs/day_12_sample_1.txt"))
    print(part_2("inputs/day_12.txt"))
