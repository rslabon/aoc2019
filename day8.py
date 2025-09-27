from collections import Counter, deque

data = "123456789012"

with open("./resources/day8.txt") as f:
    data = f.read().strip()


def create_layers(width, height, data):
    layers = []
    q = deque(data)
    for _ in range(len(data) // (width * height)):
        layer = []
        layers.append(layer)
        for i in range(height):
            row = []
            layer.append(row)
            for j in range(width):
                row.append(q.popleft())

    return layers


def part1():
    layers = create_layers(25, 6, data)
    layers = [sum(l, []) for l in layers]
    min_zero_layer = None
    min_zero_layer_value = float("inf")
    for layer in layers:
        c = Counter(layer)
        if c['0'] < min_zero_layer_value:
            min_zero_layer = layer
            min_zero_layer_value = c['0']

    c = Counter(min_zero_layer)
    print(c['1'] * c['2'])


def part2():
    layers = create_layers(25, 6, data)
    pixels = []
    for i in range(6):
        row = []
        pixels.append(row)
        for j in range(25):
            cell = ""
            for k in range(len(layers)):
                cell = layers[k][i][j]
                if cell != '2':
                    break

            row.append(cell)

    for i in range(6):
        for j in range(25):
            p = pixels[i][j]
            print("@" if p == "1" else " ", end='')
        print()


part1()
part2()
