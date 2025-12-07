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


def deal_into_new_stack(deck):
    reversed_deck = deck[::-1]
    return reversed_deck


def cut_N_cards(deck, n):
    return deck[n:] + deck[0:n]


def deal_with_increment_N(deck, n):
    new_deck = [None] * len(deck)
    i = 0
    j = 0
    while j < len(deck):
        new_deck[i] = deck[j]
        deck[j] = None
        i += n
        i %= len(deck)
        j += 1

    return new_deck


def part1():
    deck = list(range(10007))
    for line in data.split("\n"):
        if line.startswith("deal into new stack"):
            deck = deal_into_new_stack(deck)
        elif line.startswith("deal with increment "):
            line = line.replace("deal with increment ", "")
            n = int(line.strip())
            deck = deal_with_increment_N(deck, n)
        elif line.startswith("cut "):
            line = line.replace("cut ", "")
            n = int(line.strip())
            deck = cut_N_cards(deck, n)

    for position, card in enumerate(deck):
        if card == 2019:
            print(position)
            break


part1()
