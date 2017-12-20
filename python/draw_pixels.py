from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import read
import os
import time

height = 600
width = 800

source = os.getcwd() + '/' + 'wolf.obj'
r = read.Read(source)
vertex, indices = r.out()
v_max = np.max(vertex, axis=0)
v_min = np.min(vertex, axis=0)
zoom = np.max((v_max - v_min)[0:2] / [width, height])
vertex -= v_min
vertex /= zoom

tri_v = vertex[indices]
act_v = np.array([])
act_l = np.array([])
colors = np.full(indices.shape, 0.07)
zbuffer = np.zeros(width)
pixels = np.zeros((height, width, 3))

start = time.time()

for i in range(tri_v.shape[0]):
    tri_v[i] = tri_v[i, np.argsort(tri_v[:, :, 1], axis=1)[i, ::-1]]
# tri_v = tri_v[np.argsort(tri_v[:, 0, 1])[::-1]]

dx_0 = tri_v[:, 1, 0:2] - tri_v[:, 2, 0:2]
dx_0[dx_0[:, 1] == 0] = 1
dx_0 /= dx_0[:, 1].reshape(-1, 1)
dx_1 = tri_v[:, 0, 0:2] - tri_v[:, 2, 0:2]
dx_1 /= dx_1[:, 1].reshape(-1, 1)
dx_2 = tri_v[:, 0, 0:2] - tri_v[:, 1, 0:2]
dx_2[dx_2[:, 1] == 0] = 1
dx_2 /= dx_2[:, 1].reshape(-1, 1)
dx = np.concatenate((dx_0[:, 0], dx_1[:, 0], dx_2[:, 0])).reshape(3, 1, -1).T

xl = np.array([
    [0, 1, 1],
    [-1, 0, -1],
    [-1, -1, 0]
])

A_v = np.concatenate((tri_v[:, 0:3, 0:2], np.ones((tri_v.shape[0], 3, 1),)), axis=2)
b_v = tri_v[:, 0:3, 2]
solve_v = np.linalg.solve(A_v, b_v).reshape(-1, 1, 3)

tri_v = np.concatenate((tri_v, dx, solve_v), axis=1)

for i in range(int(max(vertex[:, 1])), -1, -1):
    tran = (tri_v[:, 0, 1] > i) * (tri_v[:, 0, 1] < i + 1)
    act_v = np.append(act_v, tri_v[tran]).reshape(-1, 5, 3)
    act_v = act_v[act_v[:, 2, 1] < i]
    if np.size(act_v) == 0:
        continue
    act_v1 = act_v[act_v[:, 1, 1] < i]
    act_v2 = act_v[act_v[:, 1, 1] >= i]
    j_12 = (i - act_v2[:, 0, 1]) * act_v2[:, 3, 1] + act_v2[:, 0, 0]
    j_0 = (i - act_v2[:, 2, 1]) * act_v2[:, 3, 0] + act_v2[:, 2, 0]
    j_11 = (i - act_v1[:, 0, 1]) * act_v1[:, 3, 1] + act_v1[:, 0, 0]
    j_2 = (i - act_v1[:, 0, 1]) * act_v1[:, 3, 2] + act_v1[:, 0, 0]
    j_120 = np.concatenate((j_12, j_11, j_0, j_2)).reshape(2, -1).T
    j_120 = np.sort(j_120)
    j_120 = np.ceil(j_120)

    for n in j_120:
        for j in range(int(n[0]), int(n[1])):
            # z = np.dot(act_v[:, 4], [j, i, 1])
            pixels[i, j] = [0.7, 0.7, 0.7]

elapsed = time.time() - start

print(act_v.shape)

print(elapsed)


def display():

    global pixels

    glClear(GL_COLOR_BUFFER_BIT)
   
    glDrawPixels(width, height, GL_RGB, GL_FLOAT, pixels)
    glutSwapBuffers()


def keyboard(*args):
    if args:
        exit()


def init():

    glClearColor(0, 0, 0, 0)


def main():

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(width, height)
    glutCreateWindow("Draw Pixels")
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    init()
    glutMainLoop()


main()

