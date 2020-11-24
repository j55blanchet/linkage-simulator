import matplotlib.pyplot as plt
import numpy
from sympy import Matrix
from sympy import Transpose

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tuple = [y, x]


def get_constraint_matrix(x1, y1, x2, y2, x3, y3, x4, y4):
    matrix = Matrix([[x1, 0, 0, 0, y1, 0, 0, 0], [x1-x2, x2-x1, 0, 0, y1-y2, y2-y1, 0, 0], [0, x2-x3, x3-x2, 0, 0, y2-y3, y3-y2, 0], [0, 0, x3-x4, x4-x3, 0, 0, y3-y4, y4-y3], [0, 0, 0, x4, 0, 0, 0, y4]])
    return matrix

def get_null_space(x1, y1, x2, y2, x3, y3, x4, y4):
    matrix = get_constraint_matrix(x1, y1, x2, y2, x3, y3, x4, y4)
    print(matrix)
    return matrix.nullspace()


def get_null_space_sum(x1, y1, x2, y2, x3, y3, x4, y4):
    matrix = get_constraint_matrix(x1, y1, x2, y2, x3, y3, x4, y4)
    null_space = matrix.nullspace()



    for i in range(3):
        max_index = max_matrix(null_space, i)
        max_val = null_space[i][max_index]

        for j in range(8):
            null_space[i][j] = null_space[i][j] / max_val

    return Matrix([null_space[0][0]+null_space[1][0]+null_space[2][0], null_space[0][1]+null_space[1][1]+null_space[2][1], null_space[0][2]+null_space[1][2]+null_space[2][2],
                   null_space[0][3] + null_space[1][3] + null_space[2][3], null_space[0][4]+null_space[1][4]+null_space[2][4], null_space[0][5]+null_space[1][5]+null_space[2][5],
                   null_space[0][6] + null_space[1][6] + null_space[2][6], null_space[0][7]+null_space[1][7]+null_space[2][7]])






def error(x, y):
    return x * x + y * y - 1

def max_matrix(matrix, i):
    max_index = 0
    max = abs(matrix[i][0])
    for j in range(8):
        if abs(matrix[i][j]) > max:
            max_index = j
            max = abs(matrix[i][j])

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


def plot(timestep, delta, start_x1, start_y1, start_x2, start_y2, start_x3, start_y3, start_x4, start_y4):
    anchor_point = Point(0, 0)

    flip = 0

    move_point_1 = Point(start_x1, start_y1)
    move_point_2 = Point(start_x2, start_y2)
    move_point_3 = Point(start_x3, start_y3)
    move_point_4 = Point(start_x4, start_y4)


    while True:
        plt.axis([-5, 5, -5, 5])

        null_space_sum = get_null_space_sum(move_point_1.x, move_point_1.y, move_point_2.x, move_point_2.y, move_point_3.x, move_point_3.y, move_point_4.x, move_point_4.y)



        # print(str(null_space[0][0]) +", " + str(null_space[0][1]))
        print("ERROR: " + str(error(move_point_1.x, move_point_1.y)))


        if (flip==0):
            flip = 1
        else:
            flip = 0


        move_point_1.x += delta * null_space_sum[0]
        move_point_2.x += delta * null_space_sum[1]
        move_point_3.x += delta * null_space_sum[2]
        move_point_4.x += delta * null_space_sum[3]

        move_point_1.y += delta * null_space_sum[4]
        move_point_2.y += delta * null_space_sum[5]
        move_point_3.y += delta * null_space_sum[6]
        move_point_4.y += delta * null_space_sum[7]

        plt.plot([anchor_point.x, move_point_1.x, move_point_2.x, move_point_3.x, move_point_4.x, anchor_point.x],
                 [anchor_point.y, move_point_1.y, move_point_2.y, move_point_3.y, move_point_4.y, anchor_point.y])
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

plot(0.001, 0.005, 1, 0, 1, 1, 0.5, 1.866, 0, 1)



plot_test(0.1)