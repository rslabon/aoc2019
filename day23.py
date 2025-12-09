import threading
from collections import deque

from day5 import execute

with open("resources/day23.txt") as f:
    program = [int(c) for c in f.read().strip().split(",")]


def computer(program, address, bus, stop_event):
    def get_input():
        nonlocal address, bus

        if stop_event.is_set():
            raise Exception("Stop requested")

        if not bus[address]:
            return -1

        return bus[address].popleft()

    buffer = []

    def handle_output(value):
        nonlocal buffer
        buffer.append(value)
        if len(buffer) == 3:
            # print(f"{address} is sending to {buffer[0]} X={buffer[1]}, Y={buffer[2]}")
            if buffer[0] == 255:
                print("255 Y=", buffer[2])
                stop_event.set()
                raise Exception()

            bus[buffer[0]].append(buffer[1])
            bus[buffer[0]].append(buffer[2])
            buffer = []

    try:
        execute(program, get_input, handle_output)
    except Exception:
        stop_event.set()


def part1():
    bus = [deque([i]) for i in range(50)]
    stop_event = threading.Event()
    threads = []
    for i in range(50):
        t = threading.Thread(target=computer, args=(program[:], i, bus, stop_event))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


part1()
