import math


class Vector3:
    def __init__(self, data):
        self.data = data

    def __add__(self, value):
        return Vector3([self.data[0] + value.data[0], self.data[1] + value.data[1], self.data[2] + value.data[2]])

    def __sub__(self, value):
        return Vector3([self.data[0] - value.data[0], self.data[1] - value.data[1], self.data[2] - value.data[2]])

    def __mul__(self, value):
        return self.data[0] * value.data[0] + self.data[1] * value.data[1] + self.data[2] * value.data[2]

    def normalize(self):
        if abs(self.data[0]) > abs(self.data[1]) and abs(self.data[0]) > abs(self.data[2]):
            self.data[1] /= abs(self.data[0])
            self.data[2] /= abs(self.data[0])
            self.data[0] = sign(self.data[0])
        elif abs(self.data[1]) > abs(self.data[0]) and abs(self.data[1]) > abs(self.data[2]):
            self.data[0] /= abs(self.data[1])
            self.data[2] /= abs(self.data[1])
            self.data[1] = sign(self.data[1])
        else:
            self.data[0] /= abs(self.data[2])
            self.data[1] /= abs(self.data[2])
            self.data[2] = sign(self.data[2])
        return self

    def __str__(self):
        return "(" + "{0:.2f}".format(round(self.data[0], 2)) + ", " + "{0:.2f}".format(
            round(self.data[1], 2)) + ", " + "{0:.2f}".format(round(self.data[2], 2)) + ")"


def sign(x):
    if x <= 0:
        return -1
    else:
        return 1


def cap(x, low, high):
    if x < low:
        return low
    elif x > high:
        return high
    else:
        return x


def angleTo(target_vector, origin_vector):
    difference = target_vector - origin_vector
    return math.atan2(difference.data[1], difference.data[0])


def velocity2d(velocity_vector):
    return math.sqrt(velocity_vector.data[0] ** 2 + velocity_vector.data[1] ** 2)


def distance2d(target_vector, origin_vector):
    difference = target_vector - origin_vector
    return math.sqrt(difference.data[0] ** 2 + difference.data[1] ** 2)


def calc_local_vector(vector, transformation_matrix):
    x = vector * transformation_matrix[0]
    y = vector * transformation_matrix[1]
    z = vector * transformation_matrix[2]
    return Vector3([x, y, z])


def calc_rotation_matrix(rotation_vector):
    CR = math.cos(rotation_vector[2])
    SR = math.sin(rotation_vector[2])
    CP = math.cos(rotation_vector[0])
    SP = math.sin(rotation_vector[0])
    CY = math.cos(rotation_vector[1])
    SY = math.sin(rotation_vector[1])

    matrix = [Vector3([CP * CY, CP * SY, SP]), Vector3([CY * SP * SR - CR * SY, SY * SP * SR + CR * CY, -CP * SR]),
              Vector3([-CR * CY * SP - SR * SY, -CR * SY * SP + SR * CY, CP * CR])]
    return matrix
