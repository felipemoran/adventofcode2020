from collections import namedtuple, defaultdict
import parse

# class Passport:
#     def __init__(
#         self,
#         byr=None,
#         iyr=None,
#         eyr=None,
#         hgt=None,
#         hcl=None,
#         ecl=None,
#         pid=None,
#         cid=None,
#     ):
#         self.byr = byr
#         self.iyr = iyr
#         self.eyr = eyr
#         self.hgt = hgt
#         self.hcl = hcl
#         self.ecl = ecl
#         self.pid = pid
#         self.cid = cid
#
#     def is_valid(self, exceptions):
#         self_dict = self.__dict__
#         for key in self_dict:
#             print(key)
#             value = self_dict[key]
#             if key not in exceptions or value is None:
#                 return False
#         return True

Passport = namedtuple("Passport", "byr, iyr, eyr, hgt, hcl, ecl, pid, cid")
Passport.__new__.__defaults__ = (None,) * len(Passport._fields)


def parse_file(file):
    passports = [{}]

    for line in file.read().splitlines():
        if line == "":
            passports += [{}]
            continue

        for item in line.split(" "):
            if item == "":
                continue
            key, value = item.split(":")
            passports[-1][key] = value

    passports = [Passport(**item) for item in passports]
    return passports


def value_is_valid(type, value):
    try:
        if type == "byr":
            assert len(value) == 4
            result = parse.parse("{:d}", value)
            assert 1920 <= result[0] <= 2002
        elif type == "iyr":
            assert len(value) == 4
            assert 2010 <= int(value) <= 2020
        elif type == "eyr":
            assert len(value) == 4
            assert 2020 <= int(value) <= 2030
        elif type == "hgt":
            result = parse.parse("{value:d}{unit}", value)
            assert result["unit"] in ["cm", "in"]
            if result["unit"] == "cm":
                assert 150 <= result["value"] <= 193
            elif result["unit"] == "in":
                assert 59 <= result["value"] <= 76
        elif type == "hcl":
            assert len(value) == 7
            result = parse.parse("#{value}", value)
            assert all(char in "1234567890abcdef" for char in result["value"])
        elif type == "ecl":
            assert value in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
        elif type == "pid":
            assert len(value) == 9
            int(value)
        elif type == "cid":
            pass
        return True
    except (ValueError, AssertionError):
        return False


def passport_is_valid(passport, exceptions=None):
    if exceptions is None:
        exceptions = []

    for key, value in zip(passport._fields, passport):
        if key in exceptions:
            continue
        if value is None:
            return False
        if not value_is_valid(key, value):
            return False
    return True


def part_1():
    with open("inputs/day_4.txt", "r") as file:
        passports = parse_file(file)

    counter = 0
    for passport in passports:
        if passport_is_valid(passport, exceptions=["cid"]):
            counter += 1

    return counter


if __name__ == "__main__":
    print(part_1())
