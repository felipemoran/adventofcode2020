from collections import defaultdict
from copy import copy

import parse


class Memory:
    def __init__(self, address_size=36, word_size=36):
        self._memory = defaultdict(lambda: 0, {})
        self._mask_ones = None
        self._mask_zeros = None
        self._mask_x = None
        self.word_size = word_size
        self.address_size = address_size

    def set_mask(self, raw_mask):
        self._mask_zeros = int(self._detect_values_in_mask(raw_mask, "0"), 2)
        self._mask_ones = int(self._detect_values_in_mask(raw_mask, "1"), 2)
        self._mask_x = int(self._detect_values_in_mask(raw_mask, "X"), 2)

    def set_value(self, address, value, use_mask_on=None):
        if use_mask_on is None:
            self._memory[address] = value
            return

        if use_mask_on == "value":
            value = self._apply_mask_to_value(value)
            self._memory[address] = value
            return

        elif use_mask_on == "address":
            addresses = self._apply_mask_to_address(address)
            for address in addresses:
                self._memory[address] = value

    def _apply_mask_to_value(self, value):
        if self._mask_ones is not None:
            value = self._mask_ones | value
        if self._mask_zeros is not None:
            value = (~self._mask_zeros + 2 ** self.word_size) & value
        return value

    def _apply_mask_to_address(self, address):
        if self._mask_ones is not None:
            address = self._mask_ones | address
        address = f"{address:036b}"

        x_counter = 0
        if self._mask_x is not None:
            for index, char in enumerate(char for char in f"{self._mask_x:036b}"):
                if char == "1":
                    x_counter += 1
                    # address[index] = "X"
                    address = address[:index] + "X" + address[index + 1 :]

        if x_counter == 0:
            return [int(address, 2)]

        for i in range(2 ** x_counter):
            bin_i = f"{i:0{x_counter}b}"
            address_copy = copy(address)
            for index, bit in enumerate(char for char in bin_i):
                address_copy = bit.join(address_copy.split("X", 1))
            yield int(address_copy, 2)

    def _detect_values_in_mask(self, raw_mask, target):
        return "".join("1" if item == target else "0" for item in raw_mask)


class WriteCommand:
    def __init__(self, position, value):
        self.position = position
        self.value = value


class ValueMaskCommand:
    def __init__(self, mask):
        self.mask = mask


class CommandParser:
    @classmethod
    def parse(self, raw_command):
        raw_command = raw_command.split(" = ")
        if raw_command[0] == "mask":
            return ValueMaskCommand(raw_command[1])
        elif "mem" in raw_command[0]:
            position = parse.parse("mem[{:d}]", raw_command[0])[0]
            value = int(raw_command[1])
            return WriteCommand(position, value)
        else:
            raise ValueError


def part_1(filename):
    with open(filename, "r") as file:
        commands = [CommandParser.parse(line) for line in file.read().splitlines()]

    mem = Memory()
    for command in commands:
        if isinstance(command, ValueMaskCommand):
            mem.set_mask(command.mask)
        elif isinstance(command, WriteCommand):
            mem.set_value(command.position, command.value, use_mask_on="value")
        else:
            raise ValueError

    acc = 0
    for item in mem._memory.values():
        acc += item

    return acc


def part_2(filename):
    with open(filename, "r") as file:
        commands = [CommandParser.parse(line) for line in file.read().splitlines()]

    mem = Memory()
    for command in commands:
        if isinstance(command, ValueMaskCommand):
            mem.set_mask(command.mask)
        elif isinstance(command, WriteCommand):
            mem.set_value(command.position, command.value, use_mask_on="address")
        else:
            raise ValueError

    acc = 0
    for item in mem._memory.values():
        acc += item

    return acc


if __name__ == "__main__":
    assert part_1("inputs/day_14_sample_1.txt") == 165
    print(part_1("inputs/day_14.txt"))

    assert part_2("inputs/day_14_sample_2.txt") == 208
    print(part_2("inputs/day_14.txt"))
