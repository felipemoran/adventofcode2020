from parse import parse


def parse_seat(zone):
    assert len(zone) == 10
    row_zone = zone[:7]
    seat_zone = zone[7:]

    row_zone = row_zone.replace("F", "0")
    row_zone = row_zone.replace("B", "1")
    seat_zone = seat_zone.replace("L", "0")
    seat_zone = seat_zone.replace("R", "1")

    row_number = parse("{:b}", row_zone)[0]
    seat_number = parse("{:b}", seat_zone)[0]

    return row_number * 8 + seat_number


def parse_seat_file():
    with open("inputs/day_5.txt", "r") as file:
        ids = []
        for row in file.read().splitlines():
            id = parse_seat(row)
            ids += [id]
    return ids


def gap_in_list():
    ids = sorted(parse_seat_file())
    last_id = None

    for id in ids:
        if last_id is None:
            last_id = id
            continue
        if id - last_id > 1:
            return id - 1
        last_id = id


if __name__ == "__main__":
    assert parse_seat("FBFBBFFRLR") == 357
    assert parse_seat("BFFFBBFRRR") == 567
    assert parse_seat("FFFBBBFRRR") == 119
    assert parse_seat("BBFFBBFRLL") == 820

    print(max(parse_seat_file()))
    print(gap_in_list())
