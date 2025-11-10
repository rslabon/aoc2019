import copy
from math import gcd

positions = [
    [-1, 0, 2],
    [2, -10, -7],
    [4, -8, 8],
    [3, 5, -1]
]

# positions = [
#     [-8, -10, 0],
#     [5, 5, 10],
#     [2, -7, 3],
#     [9, -8, -3]
# ]

positions = [
    [-16, 15, -9],
    [-14, 5, 4],
    [2, 0, 6],
    [-3, 18, 9]
]

velocity = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


def apply_gravity(positions, velocity):
    for i, position in enumerate(positions):
        x, y, z = position
        for j, other_position in enumerate(positions):
            if i != j:
                ox, oy, oz = other_position
                if x > ox:
                    velocity[i][0] -= 1
                elif x < ox:
                    velocity[i][0] += 1
                if y > oy:
                    velocity[i][1] -= 1
                elif y < oy:
                    velocity[i][1] += 1
                if z > oz:
                    velocity[i][2] -= 1
                elif z < oz:
                    velocity[i][2] += 1


def apply_velocity(positions, velocity):
    for i, position in enumerate(positions):
        positions[i][0] += velocity[i][0]
        positions[i][1] += velocity[i][1]
        positions[i][2] += velocity[i][2]


def energy(positions, velocity):
    sum_of_energy = 0
    for i, _ in enumerate(positions):
        pot = abs(positions[i][0]) + abs(positions[i][1]) + abs(positions[i][2])
        kin = abs(velocity[i][0]) + abs(velocity[i][1]) + abs(velocity[i][2])
        total = pot * kin
        sum_of_energy += total

    return sum_of_energy


def lcm(numbers):
    result = 1
    for i in numbers:
        result = result * i // gcd(result, i)
    return result


def part1():
    sum_of_energy = None
    for i in range(1000):
        apply_gravity(positions, velocity)
        apply_velocity(positions, velocity)
        sum_of_energy = energy(positions, velocity)

    assert sum_of_energy == 10664


def part2():
    original_positions = copy.deepcopy(positions)
    original_velocity = copy.deepcopy(velocity)

    step = 0
    cycle_length_x = None
    cycle_length_y = None
    cycle_length_z = None
    first_repeat_x = None
    first_repeat_y = None
    first_repeat_z = None

    for i in range(500_000):
        apply_gravity(positions, velocity)
        apply_velocity(positions, velocity)
        step += 1

        if positions[0][0] == original_positions[0][0] \
                and positions[1][0] == original_positions[1][0] \
                and positions[1][0] == original_positions[1][0] \
                and positions[1][0] == original_positions[1][0] \
                and velocity[0][0] == original_velocity[0][0] \
                and velocity[1][0] == original_velocity[1][0] \
                and velocity[2][0] == original_velocity[2][0] \
                and velocity[3][0] == original_velocity[3][0]:
            if not cycle_length_x and first_repeat_x:
                cycle_length_x = step - first_repeat_x
            else:
                first_repeat_x = step
        if positions[0][1] == original_positions[0][1] \
                and positions[1][1] == original_positions[1][1] \
                and positions[1][1] == original_positions[1][1] \
                and positions[1][1] == original_positions[1][1] \
                and velocity[0][1] == original_velocity[0][1] \
                and velocity[1][1] == original_velocity[1][1] \
                and velocity[2][1] == original_velocity[2][1] \
                and velocity[3][1] == original_velocity[3][1]:
            if not cycle_length_y and first_repeat_y:
                cycle_length_y = step - first_repeat_y
            else:
                first_repeat_y = step
        if positions[0][2] == original_positions[0][2] \
                and positions[1][2] == original_positions[1][2] \
                and positions[1][2] == original_positions[1][2] \
                and positions[1][2] == original_positions[1][2] \
                and velocity[0][2] == original_velocity[0][2] \
                and velocity[1][2] == original_velocity[1][2] \
                and velocity[2][2] == original_velocity[2][2] \
                and velocity[3][2] == original_velocity[3][2]:
            if not cycle_length_z and first_repeat_z:
                cycle_length_z = step - first_repeat_z
            else:
                first_repeat_z = step

    result = lcm([cycle_length_x, cycle_length_y, cycle_length_z])
    assert result == 303459551979256


part1()
part2()
