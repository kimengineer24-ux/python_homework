# Task 5: Extending a Class

import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def distance_to(self, other):
        x_difference = self.x - other.x
        y_difference = self.y - other.y
        return math.sqrt(x_difference ** 2 + y_difference ** 2)


class Vector(Point):
    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)


point1 = Point(1, 2)
point2 = Point(4, 6)
point3 = Point(1, 2)

print(point1)
print(point2)
print(point1 == point2)
print(point1 == point3)
print(point1.distance_to(point2))

vector1 = Vector(2, 3)
vector2 = Vector(4, 5)
vector3 = vector1 + vector2

print(vector1)
print(vector2)
print(vector3)