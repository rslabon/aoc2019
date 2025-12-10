import threading
from collections import deque, defaultdict

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
            if buffer[0] == 255:
                print(f"part1={buffer[2]}")
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


class Bus:
    def __init__(self):
        self.lock = threading.Lock()
        self.addresses = [deque([]) for _ in range(50)]

    def send(self, address, packet):
        with self.lock:
            self.addresses[address].append(packet)

    def peek(self, address):
        with self.lock:
            return self.addresses[address][0]

    def pop(self, address):
        with self.lock:
            return self.addresses[address].popleft()

    def has_data_for(self, address):
        with self.lock:
            return len(self.addresses[address]) != 0

    def empty(self):
        with self.lock:
            return sum(map(len, self.addresses)) == 0


class Packet:
    def __init__(self, sender_address, X, Y):
        self.sender_address = sender_address
        self.data = deque([X, Y])

    def __repr__(self):
        return f"Packet {self.sender_address}, {self.data}"


class NAT:
    def __init__(self, bus):
        self.bus = bus
        self.memory = None
        self.input_requests = defaultdict(int)
        self.lock = threading.Lock()

    def push_XY(self, X, Y):
        with self.lock:
            self.memory = (X, Y)

    def notify_idle(self, address):
        with self.lock:
            self.input_requests[address] += 1

    def notify_working(self, address):
        with self.lock:
            self.input_requests[address] = 0

    def check_idle(self):
        with self.lock:
            exceeded_input_requests = all([r >= 3 for r in self.input_requests.values()])
            if self.memory and self.bus.empty() and exceeded_input_requests:
                self.input_requests[0] = 0
                self.bus.send(0, Packet(255, self.memory[0], self.memory[1]))
                self.memory = None


def computer_with_nat(program, nat, address, bus, stop_event):
    current_packet = None
    nat_packet = []
    booting = True

    def get_input():
        nonlocal address, bus, nat, current_packet, nat_packet, booting

        if stop_event.is_set():
            raise Exception("Stop requested")

        if booting:
            booting = False
            return address

        if not current_packet and not bus.has_data_for(address):
            nat.notify_idle(address)
            nat.check_idle()
            return -1

        nat.notify_working(address)

        if not current_packet:
            current_packet = bus.peek(address)
            if address == 0 and current_packet.sender_address == 255:
                nat_packet.append(list(current_packet.data))
                if len(nat_packet) >= 2 and nat_packet[-1][1] == nat_packet[-2][1]:
                    print(f"part2={nat_packet[-1][1]}")
                    stop_event.set()
                    raise Exception()

        value = current_packet.data.popleft()
        if not current_packet.data:
            current_packet = None
            bus.pop(address)
        return value

    buffer = []

    def handle_output(value):
        nonlocal buffer, nat, address
        buffer.append(value)
        if len(buffer) == 3:
            nat.notify_working(address)
            if buffer[0] == 255:
                nat.push_XY(buffer[1], buffer[2])
            else:
                bus.send(buffer[0], Packet(buffer[0], buffer[1], buffer[2]))
            buffer = []

    try:
        execute(program, get_input, handle_output)
    except Exception:
        stop_event.set()


def part2():
    bus = Bus()
    stop_event = threading.Event()
    threads = []
    nat = NAT(bus)
    for i in range(50):
        t = threading.Thread(target=computer_with_nat, args=(program[:], nat, i, bus, stop_event))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


part1()
part2()
