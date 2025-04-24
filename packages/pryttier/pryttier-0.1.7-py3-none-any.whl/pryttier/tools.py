import math
import time
from functools import partial
import random
from typing import *
from .math import Vector2, Vector3


class Infix(object):
    def __init__(self, func: Callable) -> None:
        self.func = func

    def __or__(self, other: Self) -> Self:
        return self.func(other)

    def __ror__(self, other: Self) -> Self:
        return Infix(partial(self.func, other))

    def __call__(self, v1, v2):
        return self.func(v1, v2)


# ===Some Infix Operations===
percentOf = Infix(lambda x, y: x / 100 * y)  # x% of y
isDivisibleBy = Infix(lambda x, y: x % y == 0)  # checks if x is divisible by y


def apply(itr: Iterable, func: Callable) -> list:
    return [func(x) for x in itr]


def apply2D(iter1: Sequence, iter2: Sequence, func: Callable) -> list:
    return [func(item1, item2) for item1, item2 in zip(iter1, iter2)]


def chunks(lst: MutableSequence, n: int):
    result = []
    for i in range(0, len(lst), n):
        result.append(lst[i:i + n])
    return result


def findCommonItems(*lsts: list) -> list:
    return list(set(lsts[0]).intersection(*lsts[1:]))

def swap(array: list, index1: int, index2: int):
    temp: int = array[index1]
    array[index1] = array[index2]
    array[index2] = temp

def hex2Dec(hx: str):
    res = 0
    n = len(hx)
    for i in range(n):
        num = hx[i]
        if num in ["a", "A"]: num = "10"
        if num in ["b", "B"]: num = "11"
        if num in ["c", "C"]: num = "12"
        if num in ["d", "D"]: num = "13"
        if num in ["e", "E"]: num = "14"
        if num in ["f", "F"]: num = "15"

        res += int(num) * 16**(n - i - 1)
    return res

class Card:
    ACE = 1
    JACK = 11
    QUEEN = 12
    KING = 13

    HEARTS = 40
    DIAMONDS = 41
    SPADE = 42
    CLOVER = 43

    RED = 20
    BLACK = 21

    def __init__(self, number: str | Self, symbol: str | Self):
        self.n = number
        self.symbol = symbol
        self.color = self.RED if self.symbol in [self.HEARTS, self.DIAMONDS] else self.BLACK

    def __repr__(self):
        num = str(self.n)
        match self.n:
            case self.ACE:
                num = "Ace"
            case self.JACK:
                num = "Jack"
            case self.QUEEN:
                num = "Queen"
            case self.KING:
                num = "King"
        sym = ""
        match self.symbol:
            case self.HEARTS:
                sym = "Hearts"
            case self.DIAMONDS:
                sym = "Diamonds"
            case self.SPADE:
                sym = "Spade"
            case self.CLOVER:
                sym = "Clover"
        return f"{num} of {sym}"

# === Random ===

class RandomInt:
    def __init__(self, start: int, stop: int):
        self.start = start
        self.stop = stop

    def get(self):
        return random.randint(self.start, self.stop)

class RandomFloat:
    def __init__(self, start: int, stop: int):
        self.start = start
        self.stop = stop

    def get(self):
        return random.uniform(self.start, self.stop)


class RandomVec2Int:
    def __init__(self, xRange: tuple[int, int], yRange: tuple[int, int]):
        self.xRange = xRange
        self.yRange = yRange

    def get(self):
        x = random.randint(self.xRange[0], self.xRange[1])
        y = random.randint(self.yRange[0], self.yRange[1])
        return Vector2(x, y)

class RandomVec3Int:
    def __init__(self, xRange: tuple[int, int], yRange: tuple[int, int], zRange: tuple[int, int]):
        self.xRange = xRange
        self.yRange = yRange
        self.zRange = zRange

    def get(self):
        x = random.randint(self.xRange[0], self.xRange[1])
        y = random.randint(self.yRange[0], self.yRange[1])
        z = random.randint(self.zRange[0], self.zRange[1])
        return Vector3(x, y, z)

class RandomVec2Float:
    def __init__(self, xRange: tuple[int | float, int | float], yRange: tuple[int | float, int | float]=None):
        self.xRange = xRange
        if yRange is None:
            self.yRange = xRange
        else:
            self.yRange = yRange

    def get(self):
        x = random.uniform(self.xRange[0], self.xRange[1])
        y = random.uniform(self.yRange[0], self.yRange[1])
        return Vector2(x, y)

class RandomVec3Float:
    def __init__(self, xRange: tuple[int, int], yRange: tuple[int, int] = None, zRange: tuple[int, int] = None):
        self.xRange = xRange
        if yRange is None and zRange is None:
            self.yRange = xRange
            self.zRange = xRange
        else:
            self.yRange = yRange
            self.zRange = zRange

    def get(self):
        x = random.uniform(self.xRange[0], self.xRange[1])
        y = random.uniform(self.yRange[0], self.yRange[1])
        z = random.uniform(self.zRange[0], self.zRange[1])
        return Vector3(x, y, z)

class RandomDir2:
    def __init__(self):
        self.dir = RandomVec2Float((0, 1))
    def get(self):
        return self.dir.get()

class RandomDir3:
    def __init__(self):
        self.dir = RandomVec3Float((0, 1))
    def get(self):
        return self.dir.get()

class RandomDir2BetweenAngles:
    def __init__(self, a1: int | float, a2: int | float):
        self.start = a1
        self.stop = a2

    def get(self):
        angle = random.uniform(self.start, self.stop)
        x = math.cos(angle)
        y = math.sin(angle)
        return Vector2(x, y)


