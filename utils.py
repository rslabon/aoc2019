import time
from functools import wraps


def measure_time(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(f"Executed: {(end - start) * 1000:.3} miliseconds")
        return result

    return wrapper


@measure_time
def fun(end):
    total = 0
    for i in range(end):
        total += i
    return total

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def create(self, name, age):
        return Person(name, age)


# fun(10000)
print(Person.create("John", 78))