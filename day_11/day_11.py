# TODO: add free seats padding
# TODO: load and parse map file
# TODO: update map. Create a copy first and update it not to make updates to original map
# TODO: compare two maps for differences
# TODO: count number of occupied seats
from copy import deepcopy
from enum import Enum
from itertools import product


class UpdatePolicy(Enum):
    ADJACENCY = "adjacency"
    VISIBILITY = "visibility"


class Seat:
    class State(Enum):
        OCCUPIED = "#"
        EMPTY = "L"
        FLOOR = "."

    def __init__(self, state):
        if isinstance(state, str):
            self.state = Seat.State(state)
        else:
            self.state = state

    def __repr__(self):
        return self.state.value

    def __eq__(self, other):
        return self.state == other.state

    def update(self, num_occupied, policy):
        if self.state == self.State.FLOOR:
            return

        if self.state == self.State.EMPTY:
            if num_occupied == 0:
                self.state = self.State.OCCUPIED
            return

        if self.state == self.State.OCCUPIED:
            if policy == UpdatePolicy.ADJACENCY:
                if num_occupied >= 4:
                    self.state = self.State.EMPTY
            else:
                if num_occupied >= 5:
                    self.state = self.State.EMPTY


class Map:
    def __init__(self, map):
        self.map = map

    @property
    def num_rows(self):
        return len(self.map)

    @property
    def num_columns(self):
        return len(self.map[0])

    def __eq__(self, other):
        if self.num_rows != other.num_rows:
            return False
        if self.num_columns != other.num_columns:
            return False

        for row, column in product(range(self.num_rows), range(self.num_columns)):
            if self.map[row][column].state != other.map[row][column].state:
                return False
        return True

    def __str__(self):
        string = ""
        for row in self.map:
            for seat in row:
                string += seat.state.value
            string += "\n"
        return string

    def update(self, policy):
        new_map = deepcopy(self.map)
        did_update = False

        for row, column in product(range(self.num_rows), range(self.num_columns)):
            occupancy = self._get_seat_occupancy(row, column, policy)
            new_map[row][column].update(occupancy, policy)
            if new_map[row][column] != self.map[row][column]:
                did_update = True

        self.map = new_map
        return did_update

    def occupied_seats(self):
        return sum(
            1 for row in self.map for seat in row if seat.state == Seat.State.OCCUPIED
        )

    def _get_seat_occupancy(self, row, column, policy):
        counter = 0
        for dir_row, dir_column in product(range(-1, 2), range(-1, 2)):
            if dir_row == 0 and dir_column == 0:
                continue

            # print(f"{row:2}, {column:2}")
            if policy == UpdatePolicy.ADJACENCY:
                if (
                    self._get_seat_state(row + dir_row, column + dir_column)
                    == Seat.State.OCCUPIED
                ):
                    counter += 1
            else:
                state = Seat.State.FLOOR
                rep_counter = 0
                while state == Seat.State.FLOOR:
                    rep_counter += 1
                    state = self._get_seat_state(
                        row + rep_counter * dir_row, column + rep_counter * dir_column
                    )
                    # print(
                    #     f"\t{row + rep_counter * dir_row:2}, {column + rep_counter * dir_column:2}"
                    # )
                if state == Seat.State.OCCUPIED:
                    counter += 1
        return counter

    def _get_seat_state(self, row, column):
        if row < 0 or column < 0 or row >= self.num_rows or column >= self.num_columns:
            return Seat.State.EMPTY
        return self.map[row][column].state


def parse_map_file(filename):
    map = []
    with open(f"inputs/{filename}", "r") as file:
        for row in file.read().splitlines():
            map += [[]]
            for seat in row:
                map[-1] += [Seat(seat)]
    return Map(map)


def run(policy, sample_num, num_steps, expected_occupied):
    map = parse_map_file(f"day_11_sample_{sample_num}_step_0.txt")
    for i in range(1, num_steps + 1):
        reference = parse_map_file(f"day_11_sample_{sample_num}_step_{i}.txt")
        did_update = map.update(policy)
        assert map == reference
        assert did_update

    did_update = map.update(policy)
    assert not did_update
    assert map.occupied_seats() == expected_occupied

    map = parse_map_file("day_11.txt")
    did_update = True

    counter = 0
    while did_update:
        counter += 1
        did_update = map.update(policy)
        print(f"Updates: {counter} Occupied: {map.occupied_seats()}")

    print(map.occupied_seats())


if __name__ == "__main__":
    # run(UpdatePolicy.ADJACENCY, 1, 5, 37)
    run(UpdatePolicy.VISIBILITY, 2, 6, 26)
