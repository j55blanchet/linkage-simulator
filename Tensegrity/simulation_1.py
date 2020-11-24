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



def plot_test(timestep):
    anchor_point = Point(0, 0)
    move_point = Point(1, 0)

    while True:
        plt.axis([-1.5, 1.5, -1.5, 1.5])
        move_point.y += 0.01
        plt.plot([anchor_point.x, move_point.x],[anchor_point.y, move_point.y])
        plt.pause(timestep)
        plt.clf()
        plt.draw()


def error(x, y):
    return x*x + y*y - 1


def plot(timestep, delta, start_x, start_y):
    anchor_point = Point(0, 0)

    move_point = Point(start_x, start_y)

    while True:
        plt.axis([-1.5, 1.5, -1.5, 1.5])

        null_space = get_null_space(move_point.x, move_point.y)

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
        if (move_point.y > 0 and null_space[0][0] > 0):
            null_space[0][0] = null_space[0][0] * -1
            null_space[0][1] = null_space[0][1] * -1

        if (move_point.y < 0 and null_space[0][1] > 0):
            null_space[0][0] = null_space[0][0] * -1
            null_space[0][1] = null_space[0][1] * -1

        if (move_point.y < 0 and move_point.x > 0 and null_space[0][0] < 0):
            null_space[0][0] = null_space[0][0] * -1
            null_space[0][1] = null_space[0][1] * -1

        # print(str(null_space[0][0]) +", " + str(null_space[0][1]))
        print("ERROR: " + str(error(move_point.x, move_point.y)))

        move_point.x += delta * null_space[0][0]
        move_point.y += delta * null_space[0][1]

        plt.plot([anchor_point.x, move_point.x], [anchor_point.y, move_point.y])
        plt.pause(timestep)
        plt.clf()
        plt.draw()


plot(0.01, 0.01, 1, 0)


#error at 1 circle = 0.0724886913017018, always increasing


