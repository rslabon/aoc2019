def compute_value(input_signal, index):
    value = 0
    offset = index - 1
    while offset < len(input_signal):
        for i in range(index):
            value += input_signal[offset]
            offset += 1
            if offset >= len(input_signal):
                return value
        offset += index
        if offset >= len(input_signal):
            return value
        for i in range(index):
            value -= input_signal[offset]
            offset += 1
            if offset >= len(input_signal):
                return value
        offset += index
    return value


def fft(input_signal):
    size = len(input_signal)
    new_signal = ["#"] * size
    for index in range(1, size + 1):
        value = compute_value(input_signal, index)
        value = int(str(value)[-1])
        new_signal[index - 1] = value

    return new_signal


def fft2(input_signal, offset):
    size = len(input_signal)
    new_signal = ["#"] * size
    last_value = None
    for index in range(offset, size + 1):
        if last_value is None:
            last_value = sum(input_signal[index - 1:])
        else:
            last_value -= input_signal[index - 2]

        value = int(str(last_value)[-1])
        new_signal[index - 1] = value

    return new_signal


def part1():
    input_signal = [int(c) for c in
                    "59738476840592413842278931183278699191914982551989917217627400830430491752064195443028039738111788940383790187992349338669216882218362200304304999723624146472831445016914494176940890353790253254035638361091058562936884762179780957079673204210602643442603213181538626042470133454835824128662952579974587126896226949714610624975813583386749314141495655816215568136392852888525754247201021383516228214171660111826524421384758783400220017148022332694799323429711845103305784628923350853888186977670136593067604033507812932778183786479207072226236705355778245701287481396364826358903409595200711678577506495998876303181569252680220083046665757597971122614"]

    for _ in range(100):
        input_signal = fft(input_signal)

    result = "".join(map(str, input_signal))[0:8]
    assert result == "74608727"


def part2():
    signal = [int(c) for c in
              "59738476840592413842278931183278699191914982551989917217627400830430491752064195443028039738111788940383790187992349338669216882218362200304304999723624146472831445016914494176940890353790253254035638361091058562936884762179780957079673204210602643442603213181538626042470133454835824128662952579974587126896226949714610624975813583386749314141495655816215568136392852888525754247201021383516228214171660111826524421384758783400220017148022332694799323429711845103305784628923350853888186977670136593067604033507812932778183786479207072226236705355778245701287481396364826358903409595200711678577506495998876303181569252680220083046665757597971122614"]
    input_signal = signal * 10_000
    offset = int("".join(map(str, input_signal[0:7])))

    for i in range(100):
        input_signal = fft2(input_signal, offset)

    msg = input_signal[offset:offset + 8]
    result = "".join(map(str, msg))
    assert result == "57920757"


part1()
part2()
