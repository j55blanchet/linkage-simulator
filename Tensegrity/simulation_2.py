import matplotlib.pyplot as plt
import numpy
from sympy import Matrix
from sympy import Transpose

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tuple = [y, x]


def get_constraint_matrix(x, y):
    matrix = Matrix([[2*x, 2*y]])
    return matrix

def get_null_space(x, y):
    matrix = get_constraint_matrix(x,y)
    return matrix.nullspace()

def get_constraint_matrix1(x1, y1):
    matrix = Matrix([[2*x1, 2*y1]])
    return matrix

def error_1(x1, y1):
    return x1 * x1 + y1 * y1 - 1

def error_2(x1, y1):
    return x1 * x1 + y1 * y1 - 1

def plot_test(timestep):
    anchor_point = Point(0, 0)
    move_point_1 = Point(1, 0)
    move_point_2 = Point(2, 0)

    while True:
        plt.axis([-2.5, 2.5, -2.5, 2.5])
        move_point_1.y += 0.01
        move_point_2.y -= 0.02
        plt.plot([anchor_point.x, move_point_1.x, move_point_2.x],[anchor_point.y, move_point_1.y, move_point_2.y])
        plt.pause(timestep)
        plt.clf()
        plt.draw()


def plot(timestep, delta, start_x1, start_y1, start_x2, start_y2):
    anchor_point = Point(0, 0)


    move_point_1 = Point(start_x1, start_y1)
    move_point_2 = Point(start_x2, start_y1)

    while True:
        plt.axis([-2.5, 2.5, -2.5, 2.5])

        null_space = get_null_space(move_point_1.x, move_point_1.y)

        # TRYING TO DEFEAT SYMPY CONVENTIONS

        if (abs(null_space[0][0]) > abs(null_space[0][1])):
            null_space[0][1] = null_space[0][1] / abs(null_space[0][0])
            if null_space[0][0] >= 0:
                null_space[0][0] = 1
            else:
                null_space[0][0] = -1

        else:
            null_space[0][0] = null_space[0][0] / abs(null_space[0][1])
            null_space[0][1] = 1
            if null_space[0][1] >= 0:
                null_space[0][1] = 1
            else:
                null_space[0][1] = -1

        # code to keep it moving counter clockwise (prevents it getting stuck in periodic motion around axes)
        if (move_point_1.y > 0 and null_space[0][0] > 0):
            null_space[0][0] = null_space[0][0] * -1
            null_space[0][1] = null_space[0][1] * -1

        if (move_point_1.y < 0 and null_space[0][1] > 0):
            null_space[0][0] = null_space[0][0] * -1
            null_space[0][1] = null_space[0][1] * -1

        if (move_point_1.y < 0 and move_point_1.x > 0 and null_space[0][0] < 0):
            null_space[0][0] = null_space[0][0] * -1
            null_space[0][1] = null_space[0][1] * -1

        # print(str(null_space[0][0]) +", " + str(null_space[0][1]))
        print("ERROR: " + str(error_1(move_point_1.x, move_point_1.y)))

        move_point_1.x += delta * null_space[0][0]
        move_point_1.y += delta * null_space[0][1]

        move_point_2.x += delta * null_space[0][0]
        move_point_2.y += delta * null_space[0][1]


        plt.plot([anchor_point.x, move_point_1.x, move_point_2.x],[anchor_point.y, move_point_1.y, move_point_2.y])
        plt.pause(timestep)
        plt.clf()
        plt.draw()


plot(0.01, 0.01, 1, 0, 2, 0)



plot_test(0.1)