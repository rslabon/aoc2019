data = """
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
""".strip()

with open("resources/day22.txt") as f:
    data = f.read().strip()


def deal_into_new_stack(size, position):
    return size - position - 1


def cut_N_cards(size, position, n):
    if n >= 0:
        return (size - n + position) % size
    return (position + abs(n)) % size


def deal_with_increment_N(size, position, n):
    return (position * n) % size


def part1():
    size = 10007
    position = 2019
    for line in data.split("\n"):
        if line.startswith("deal into new stack"):
            position = deal_into_new_stack(size, position)
        elif line.startswith("deal with increment "):
            line = line.replace("deal with increment ", "")
            n = int(line.strip())
            position = deal_with_increment_N(size, position, n)
        elif line.startswith("cut "):
            line = line.replace("cut ", "")
            n = int(line.strip())
            position = cut_N_cards(size, position, n)

    assert position == 2514


def redeal_into_new_stack(size, position):
    return deal_into_new_stack(size, position)


def recut_N_cards(size, position, n):
    if n >= 0:
        return cut_N_cards(size, position, -n)
    else:
        return cut_N_cards(size, position, -1 * size - n)


def egcd(a, b):
    if b == 0:
        return 1, 0, a
    x, y, g = egcd(b, a % b)
    return y, x - (a // b) * y, g


def modinv(a, m):
    a %= m
    x, _, g = egcd(a, m)
    if g != 1:
        raise ValueError(f"egcd({a}, {m}) != 1")
    return x % m


def redeal_with_increment_N(size, position, n):
    inv = modinv(n, size)
    return (position * inv) % size


def part2():
    size = 119315717514047
    position = 2020
    for i in range(101741582076661):
        for j, line in enumerate(reversed(data.split("\n"))):
            if line.startswith("deal into new stack"):
                position = redeal_into_new_stack(size, position)
            elif line.startswith("deal with increment "):
                line = line.replace("deal with increment ", "")
                n = int(line.strip())
                position = redeal_with_increment_N(size, position, n)
            elif line.startswith("cut "):
                line = line.replace("cut ", "")
                n = int(line.strip())
                position = recut_N_cards(size, position, n)

    print(position)


part1()
part2()
