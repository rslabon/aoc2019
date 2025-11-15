import re
from collections import defaultdict

data = """
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
""".strip().splitlines()

# with open("./resources/day14.txt") as f:
#     data = f.read().strip().splitlines()

complex_reactions = {}
for line in data:
    part1, part2 = line.split("=>")
    input_chems = part1.strip().split(",")
    inputs = []
    for chem in input_chems:
        input_value, input_name = re.findall(r"(\d+) (\w+)", chem.strip())[0]
        inputs.append((input_name, int(input_value)))
    output_value, output_name = re.findall(r"(\d+) (\w+)", part2.strip())[0]
    output_value = int(output_value)
    complex_reactions[output_name] = output_value, inputs


def create(name, complex_reactions, stock):
    if name == "ORE":
        stock["ORE"] += 1
        stock["TOTAL_ORE"] += 1
        return

    output_value, inputs = complex_reactions[name]
    for input_name, input_value in inputs:
        produce(input_name, input_value, complex_reactions, stock)

    stock[name] += output_value


def produce(name, required, complex_reactions, stock):
    while stock[name] < required:
        create(name, complex_reactions, stock)
    stock[name] -= required


def part1():
    stock = defaultdict(lambda: 0)
    produce("FUEL", 1, complex_reactions, stock)
    assert stock["TOTAL_ORE"] == 598038


def part2():
    stock = defaultdict(lambda: 0)
    fuel = 0
    while True:
        produce("FUEL", 1, complex_reactions, stock)
        if stock["TOTAL_ORE"] <= 1000000000000:
            fuel += 1
            print("FUEL", fuel, 1000000000000 - stock["TOTAL_ORE"])
        else:
            break
    print(fuel)


# part1()
part2()
