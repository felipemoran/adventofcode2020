class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, color, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if color not in cls._instances:
            instance = super().__call__(color, *args, **kwargs)
            cls._instances[color] = instance
        return cls._instances[color]


class Bag(metaclass=SingletonMeta):
    def __init__(self, color, children=None):
        self.color = color
        self.children = {} if children is None else children
        self.parents = []

    def __repr__(self):
        return f"{self.color} {self.children}"

    def add_child(self, bag, quantity):
        self.children.update({bag: quantity})

    def add_parent(self, bag):
        self.parents += [bag]

    def contains(self, bag, recursion_list=None):
        if recursion_list is None:
            recursion_list = []
        recursion_list += [self]

        for child_bag in self.children:
            if child_bag == bag:
                return True
            if child_bag in recursion_list:
                continue
            if child_bag.contains(bag, recursion_list):
                return True
        return False

    def update_parent_list(self, parent_list):
        for parent in self.parents:
            if parent in parent_list:
                continue
            parent_list.append(parent)
            parent.update_parent_list(parent_list)

    def count_child_bags(self):
        sum = 0
        for child, quantity in self.children.items():
            child_num_of_bags = child.count_child_bags()
            sum += quantity * (1 + child_num_of_bags)
        return sum


def parse_bag(bag_description):
    # example: "light red bags contain 1 bright white bag, 2 muted yellow bags."
    # format: "{color} bags contain [{int} {color}{or [", ", "."]}]

    bag_description = bag_description.replace(".", ", ")

    color, child_bag_descriptions = bag_description.split(" bags contain ")
    parent_bag = Bag(color)
    child_bag_descriptions = child_bag_descriptions.split(", ")[:-1]

    if "no other bags" in child_bag_descriptions:
        return parent_bag

    for child_bag_description in child_bag_descriptions:
        quantity, color = child_bag_description.split(" ", 1)
        quantity = int(quantity)
        color = color.split(" bag")[0]
        child_bag = Bag(color)
        parent_bag.add_child(child_bag, quantity)
        child_bag.add_parent(parent_bag)

    return parent_bag


def part_1(filename, target):
    with open(f"inputs/{filename}", "r") as file:
        lines = file.read().splitlines()

    bags = []
    for line in lines:
        new_bag = parse_bag(line)
        bags += [new_bag]

    bag = Bag(target)
    parent_list = []
    bag.update_parent_list(parent_list)

    return len(parent_list), bag.count_child_bags()


if __name__ == "__main__":
    print(part_1("day_7_sample.txt", "shiny gold"))
    SingletonMeta._instances = {}
    print(part_1("day_7_sample_2.txt", "g"))
    SingletonMeta._instances = {}
    print(part_1("day_7.txt", "shiny gold"))
    SingletonMeta._instances = {}
