import itertools
import math
from fractions import Fraction
from typing import *
from multipledispatch import dispatch
import numpy as np
from numpy import sqrt
from numpy.ma.core import arccos

PI = 2 * arccos(0)
Degrees = PI / 180


def summation(n: float | int, i: float | int, expr: Callable) -> float:
    total = 0
    for j in range(n, i + 1):
        total += expr(j)
    return total


def product(n: int, i: int, expr: Callable) -> float:
    total = 1
    for j in range(n, i):
        total *= expr(j)
    return total


def clamp(num: float, low: float, high: float) -> float:
    if num < low:
        return low
    if num > high:
        return high
    return num


def sign(num: float) -> int:
    return int(num / abs(num))


def factorial(num: int) -> int:
    if num == 0:
        return 1
    if num == 1:
        return 1
    return num * factorial(num - 1)


def mapRange(value: int | float,
             min1: float,
             max1: float,
             min2: float,
             max2: float) -> float:
    return (value - min1) / (max1 - min1) * (max2 - min2) + min2


def isPrime(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def getFactors(num: int):
    factors = []
    for i in range(1, num + 1):
        if num % i == 0:
            factors.append(i)

    return factors


def decToFraction(dec: float):
    return Fraction(dec).limit_denominator()


def radToDeg(num: float):
    return num * (180 / PI)


def degToRad(num: float):
    return num * (PI / 180)


def getDigits(num: int):
    return [int(i) for i in list(str(num))]


class SampleSpace:
    """WARNING: Not suitable for large sample spaces"""

    def __init__(self, space: list) -> None:
        self.space: list = space

    def __repr__(self):
        return str(self.space).replace("[", "{").replace("]", "}")

    def getIf(self, func: Callable[[Any], bool]) -> list:
        items = []
        for i in self.get():
            if func(i):
                items.append(i)
        return items

    def __len__(self) -> int:
        return len(self.space)

    def get(self) -> list:
        return self.space

    @classmethod
    def generate(cls, possibility: list | str, length: int, repeat: bool = True) -> Self:
        if repeat:
            combs = list(itertools.product(possibility, repeat=length))
        else:
            combs = list(itertools.permutations(possibility, r=length))

        for i in range(len(combs)):
            isStr = []
            for j in combs[i]:
                if type(j) == str:
                    isStr.append(True)
                else:
                    isStr.append(False)

            if all(isStr):
                combs[i] = "".join(combs[i])

        return SampleSpace(combs)


def probability(sampleSpace: SampleSpace, favourable: list):
    for i in favourable:
        if i not in sampleSpace.get():
            return 0
    return len(favourable) / len(sampleSpace)


class Vector2:
    def __init__(self,
                 x: float | int,
                 y: float | int):
        self.x = x
        self.y = y
        self.xy = (self.x, self.y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __add__(self, other: Self) -> Self:
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float | int) -> Self:
        return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other: float | int):
        return Vector2(self.x / other, self.y / other)

    def __iter__(self):
        return iter([self.x, self.y])

    def magnitude(self):
        return sqrt(self.x * self.x + self.y * self.y)

    def normalize(self) -> Self:
        if self.magnitude() == 0:
            return Vector2.zero()
        return Vector2(self.x / self.magnitude(), self.y / self.magnitude())

    def toInt(self):
        return Vector2(int(self.x), int(self.y))

    def __round__(self, n=None):
        return Vector2(round(self.x, n), round(self.y, n))

    def round(self, n=None):
        return Vector2(round(self.x, n), round(self.y, n))

    def toMat(self):
        mat = Matrix(2, 1)
        mat.set([[self.x], [self.y]])

    def toNumpy(self):
        return np.array([self.x, self.y])

    # ---Class Methods---
    @classmethod
    def zero(cls):
        return Vector2(0, 0)

    @classmethod
    def one(cls):
        return Vector2(1, 1)

    @classmethod
    def distance(cls, a: Self, b: Self):
        dx = b.x - a.x
        dy = b.y - a.y
        return math.sqrt(dx * dx + dy * dy)

    @classmethod
    def dot(cls, a: Self, b: Self):
        return Vector2(a.x * b.x, a.y * b.y)

    @classmethod
    def cross(cls, a: Self, b: Self):
        return a.x * b.y - a.y * b.x

    @classmethod
    def angleBetween(cls, a: Self, b: Self):
        dotProduct = cls.dot(a, b)
        magA = a.magnitude()
        magB = b.magnitude()
        return math.acos(dotProduct / (magA * magB))

    @classmethod
    def interpolate(cls, a: Self, b: Self, t: float):
        v = b - a
        pdx = a.x + v.x * t
        pdy = a.y + v.y * t
        return Vector2(pdx, pdy)


class Vector3:
    def __init__(self,
                 x: float | int,
                 y: float | int,
                 z: float | int):
        self.x = x
        self.y = y
        self.z = z
        self.xyz = (self.x, self.y, self.z)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def __add__(self, other: Self) -> Self:
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Self) -> Self:
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: float | int) -> Self:
        return Vector3(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other: float | int):
        return Vector3(self.x / other, self.y / other, self.z / other)

    def __iter__(self):
        return iter([self.x, self.y, self.z])

    def magnitude(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self) -> Self:
        if self.magnitude() == 0:
            return Vector3.zero()
        return Vector3(self.x / self.magnitude(), self.y / self.magnitude(), self.z / self.magnitude())

    def toInt(self):
        return Vector3(int(self.x), int(self.y), int(self.z))

    def __round__(self, n=None):
        return Vector3(round(self.x, n), round(self.y, n), round(self.z, n))

    def toMat(self):
        mat = Matrix(3, 1)
        mat.set([[self.x], [self.y], [self.z]])

    def toNumpy(self):
        return np.array([self.x, self.y, self.z])

    # ---Class Methods---
    @classmethod
    def zero(cls):
        return Vector3(0, 0, 0)

    @classmethod
    def one(cls):
        return Vector3(1, 1, 1)

    @classmethod
    def distance(cls, a: Self, b: Self):
        dx = b.x - a.x
        dy = b.y - a.y
        dz = b.z - a.z
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    @classmethod
    def dot(cls, a: Self, b: Self):
        return Vector3(a.x * b.x, a.y * b.y, a.z * b.z)

    @classmethod
    def cross(cls, a: Self, b: Self) -> Self:
        i = a.y * b.z - a.z * b.y
        j = a.z * b.x - a.x * b.z
        k = a.x * b.y - a.y * b.x
        return Vector3(i, j, k)

    @classmethod
    def angleBetween(cls, a: Self, b: Self):
        dotProduct = cls.dot(a, b)
        magA = a.magnitude()
        magB = b.magnitude()
        return math.acos(dotProduct / (magA * magB))

    @classmethod
    def interpolate(cls, a: Self, b: Self, t: float):
        v = b - a
        pdx = a.x + v.x * t
        pdy = a.y + v.y * t
        pdz = a.z + v.z * t
        return Vector3(pdx, pdy, pdz)

def closestFromArrayNumber(arr: Sequence[float], num: float | int):
    def difference(a):
        return abs(a - num)

    return min(arr, key=difference)


def closestFromArrayVec2(arr: Sequence[Vector2], num: Vector2):
    def difference(a: Vector2):
        return Vector2(abs(a.x - num.x), abs(a.y - num.y)).magnitude

    return min(arr, key=difference)


def closestFromArrayVec3(arr: Sequence[Vector3], num: Vector3):
    def difference(a: Vector3):
        return Vector3(a.x - num.x, a.y - num.y, a.z - num.z).magnitude

    return min(arr, key=difference)


def arrayToVec2array(arr: Sequence[Sequence[int]]):
    result = []
    for i in arr:
        if len(i) != 2:
            raise Exception("length has to be 2")
        else:
            result.append(Vector2(*i))
    return result


def arrayToVec3array(arr: Sequence[Sequence[int]]):
    result = []
    for i in arr:
        if len(i) != 3:
            raise Exception("length has to be 3")
        else:
            result.append(Vector3(*i))
    return result


def vec2arrayToArray(arr: Sequence[Vector2]):
    return [[a.x, a.y] for a in arr]


def vec3arrayToArray(arr: Sequence[Vector3]):
    return [[a.x, a.y, a.z] for a in arr]


def lerp(a, b, t: float):
    return (1 - t) * a + t * b


def lerp2D(p1: Vector2, p2: Vector2, t: float):
    return p1 + (p2 - p1) * t


def lerp3D(p1: Vector3, p2: Vector3, t: float):
    return p1 + (p2 - p1) * t


class Matrix:

    @dispatch(int, int)
    def __init__(self, r: int, c: int) -> None:
        self.rows = r
        self.cols = c
        self.matrix = np.zeros([r, c])

    @dispatch(list)
    def __init__(self, mat: np.ndarray | list[list[int | float]]) -> None:
        self.matrix = mat
        self.rows = len(mat)
        self.cols = len(mat[0])

    def set(self, mat: np.ndarray | list[list[int | float]]) -> np.ndarray | ValueError:
        matRows = len(mat)
        matCols = len(mat[0])
        if matRows == self.rows and matCols == self.cols:
            self.matrix = mat
        else:
            raise ValueError(f"Expected matrix of dimensions ({self.rows}, {self.cols}) but got ({matRows}, {matCols})")

    def __repr__(self):
        txt = [""]  # ┌┘└┐
        for i in range(self.rows):
            row = f"|{[int(self.matrix[i][j]) for j in range(self.cols)]}|\n"
            row = row.replace("[", "").replace("]", "").replace(",", "")
            txt.append(row)
        return "".join(txt)

    def __getitem__(self, item: tuple[int, int] | int):
        if type(item) == int:
            return self.matrix[item]
        elif type(item) == tuple:
            return self.matrix[item[0]][item[1]]

    def __setitem__(self, key: tuple[int, int], value: int | float):
        self.matrix[key[0]][key[1]] = value

    def __invert__(self):
        newMat = Matrix(self.cols, self.rows)
        for i in range(self.rows):
            for j in range(self.cols):
                newMat[j][i] = self.matrix[i][j]
        return newMat

    def __matmul__(self, other: Self):
        if self.cols != other.rows:
            raise TypeError(
                "Number of columns of the first matrix must be equal to number of rows of the second matrix")
        mat = Matrix(self.rows, other.cols)
        mat.matrix = np.dot(self.matrix, other.matrix)
        return mat

    def toVec(self):
        if self.cols == 2:
            return Vector2(float(self[0, 0]), float(self[0, 1]))
        elif self.cols == 3:
            return Vector3(float(self[0, 0]), float(self[0, 1]), float(self[0, 2]))

    # Class Methods
    @classmethod
    def identity(cls, r, c):
        mat = Matrix(r, c)
        for i in range(r):
            for j in range(c):
                if i == j: mat.matrix[i][j] = 1
        return mat
