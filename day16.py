import functools
from collections import defaultdict


# @functools.cache
# def transform_pattern(size, pattern, index):
#     result = []
#     while True:
#         for i in pattern:
#             for j in range(0, index):
#                 result.append(i)
#                 if len(result) - 1 == size:
#                     return result[1:]
#
#
# @functools.cache
# def transform_pattern2(size, index):
#     pattern = [0, 1, 0, -1]
#     result = []
#     while True:
#         for i in pattern:
#             for j in range(0, index):
#                 result.append(i)
#                 if len(result) - 1 == size:
#                     result = result[1:]
#                     by_value = defaultdict(list)
#                     for iv, v in enumerate(result):
#                         by_value[v].append(iv)
#
#                     return tuple(by_value[1]), tuple(by_value[-1])


@functools.cache
def transform_pattern2(size, index):
    pattern = [0, 1, 0, -1]
    result = []
    while True:
        for i in pattern:
            result += [i] * index
            if len(result) - 1 >= size:
                result = result[1:1 + size]
                by_value = defaultdict(list)
                for iv, v in enumerate(result):
                    by_value[v].append(iv)

                return result, tuple(by_value[1]), tuple(by_value[-1])


def compute_value(signal, indexes):
    value = 0
    for i in indexes:
        value += signal[i]

    return value


def fft(input_signal):
    new_signal = []
    size = len(input_signal)
    l = len("69317163492948606335995924319873")
    for index in range(1, size + 1):
        pattern, one, minus_one = transform_pattern2(size, index)
        s = {0: " ", 1: "+", -1: "-"}
        value = compute_value(input_signal, one)
        value -= compute_value(input_signal, minus_one)
        print("Index: ", index, value)

        for i in range(0, len(input_signal), l):
            print("".join(map(str, input_signal[i:i+l])), end="|")
        print()
        for i in range(0, len(input_signal), l):
            print("".join(map(lambda v: s[v], pattern[i:i+l])), end="|")
        print()

        value = int(str(value)[-1])
        new_signal.append(value)



    return new_signal


def part1():
    input_signal = [int(c) for c in
                    "59738476840592413842278931183278699191914982551989917217627400830430491752064195443028039738111788940383790187992349338669216882218362200304304999723624146472831445016914494176940890353790253254035638361091058562936884762179780957079673204210602643442603213181538626042470133454835824128662952579974587126896226949714610624975813583386749314141495655816215568136392852888525754247201021383516228214171660111826524421384758783400220017148022332694799323429711845103305784628923350853888186977670136593067604033507812932778183786479207072226236705355778245701287481396364826358903409595200711678577506495998876303181569252680220083046665757597971122614"]

    for _ in range(100):
        input_signal = tuple(fft(tuple(input_signal)))

    result = "".join(map(str, input_signal))[0:8]
    assert result == "74608727"


def part2():
    signal = [int(c) for c in "69317163492948606335995924319873"]
    input_signal = signal * 5
    offset = int("".join(map(str, input_signal[0:7])))

    # size = len(input_signal)
    # for index in range(1, size + 1):
    #     print("pattern", index)
    #     transform_pattern2(size, index)

    for i in range(10):
        print(f"processing {i}")
        input_signal = tuple(fft(tuple(input_signal)))

    msg = input_signal[offset:offset + 8]
    result = "".join(map(str, msg))
    print(result)  # 53553731
    # print("".join(map(str, input_signal))[0:8])


# part1()
part2()

# size = 651 * 10_000
# for index in range(1, size + 1):
#     print("pattern", index)
#     transform_pattern2(size, index)
