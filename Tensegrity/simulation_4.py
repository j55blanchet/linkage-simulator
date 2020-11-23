import matplotlib.pyplot as plt
import numpy
from sympy import Matrix
from sympy import Transpose

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tuple = [y, x]


def get_constraint_matrix(x1, y1, x2, y2, x3, y3):
    matrix = Matrix([[x1, 0, 0, y1, 0, 0], [x1-x2, x2-x1, 0, y1-y2, y2-y1, 0], [0, x2-x3, x3-x2, 0, y2-y3, y3-y2], [0, 0, x3, 0, 0, y3]])
    return matrix

def get_null_space(x1, y1, x2, y2, x3, y3):
    matrix = get_constraint_matrix(x1, y1, x2, y2, x3, y3)
    print(matrix)
    return matrix.nullspace()


def error(x, y):
    return x * x + y * y - 1

def max_matrix(matrix):
    max_index = 0
    max = abs(matrix[0][0])
    for i in range(5):
        if abs(matrix[0][i]) > max:
            max_index = i
            max = abs(matrix[0][i])

    return max_index


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


def plot(timestep, delta, start_x1, start_y1, start_x2, start_y2, start_x3, start_y3):
    anchor_point = Point(0, 0)

    flip = 0

    move_point_1 = Point(start_x1, start_y1)
    move_point_2 = Point(start_x2, start_y2)
    move_point_3 = Point(start_x3, start_y3)

    while True:
        plt.axis([-5, 5, -5, 5])

        null_space = get_null_space(move_point_1.x, move_point_1.y, move_point_2.x, move_point_2.y, move_point_3.x, move_point_3.y)

        max_index = max_matrix(null_space)
        max_val = null_space[0][max_index]

        for i in range(5):
            null_space[0][i] = null_space[0][i] / max_val


        # print(str(null_space[0][0]) +", " + str(null_space[0][1]))
        print("ERROR: " + str(error(move_point_1.x, move_point_1.y)))


        if (flip==0):
            flip = 1
        else:
            flip = 0

        print(null_space)
        move_point_1.x += delta * null_space[0][0]
        move_point_2.x += delta * null_space[0][1]
        move_point_3.x += delta * null_space[0][2]

        move_point_1.y += delta * null_space[0][3]
        move_point_2.y += delta * null_space[0][4]
        move_point_3.y += delta * null_space[0][5]

        plt.plot([anchor_point.x, move_point_1.x, move_point_2.x, move_point_3.x, anchor_point.x],
                 [anchor_point.y, move_point_1.y, move_point_2.y, move_point_3.y, anchor_point.y])
        plt.pause(timestep)
        plt.clf()
        plt.draw()

        '''
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
        '''

        # TRYING TO DEFEAT SYMPY CONVENTIONS

plot(0.001, 0.01, 1, 0, 1, 1, 0, 1)



plot_test(0.1)