import functools


@functools.cache
def transform_pattern(size, pattern, index):
    result = []
    while True:
        for i in pattern:
            for j in range(0, index):
                result.append(i)
                if len(result) - 1 == size:
                    return result[1:]


def fft(input_signal, pattern):
    size = len(input_signal)
    new_signal = []
    for index in range(1, size + 1):
        pattern_for_index = transform_pattern(size, tuple(pattern), index)
        value = 0
        for j in range(size):
            value += input_signal[j] * pattern_for_index[j]

        value = int(str(value)[-1])
        new_signal.append(value)

    return new_signal


def part1():
    input_signal = [int(c) for c in
                    "59738476840592413842278931183278699191914982551989917217627400830430491752064195443028039738111788940383790187992349338669216882218362200304304999723624146472831445016914494176940890353790253254035638361091058562936884762179780957079673204210602643442603213181538626042470133454835824128662952579974587126896226949714610624975813583386749314141495655816215568136392852888525754247201021383516228214171660111826524421384758783400220017148022332694799323429711845103305784628923350853888186977670136593067604033507812932778183786479207072226236705355778245701287481396364826358903409595200711678577506495998876303181569252680220083046665757597971122614"]
    pattern = [int(c.strip()) for c in "0, 1, 0, -1".split(",")]

    for _ in range(100):
        input_signal = fft(input_signal, pattern)

    result = "".join(map(str, input_signal))[0:8]
    assert result == "74608727"


def part2():
    input_signal = [int(c) for c in "03036732577212944063491565474664"]
    pattern = [int(c.strip()) for c in "0, 1, 0, -1".split(",")]

    for _ in range(1):
        input_signal = fft(input_signal, pattern)

    msg = "".join(map(str, input_signal))
    offset = int(msg[0:7])
    result = msg[offset:offset + 8]
    print(result)


part1()
# part2()
