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

vertex[:, 0:2] = np.floor(vertex[:, 0:2])

tri_v = vertex[indices]
act_v = np.array([])
act_l = np.array([])
colors = np.full(indices.shape, 0.07)
zbuffer = np.zeros(width)
pixels = np.zeros((height, width, 3))

light_pos = np.array([width, height, max(vertex[:, 2])])
light_color = np.array([1, 1, 1])
object_color = np.array([1, 1, 0])

start = time.time()

for i in range(tri_v.shape[0]):
    tri_v[i] = tri_v[i, np.argsort(tri_v[:, :, 1], axis=1)[i, ::-1]]

dx_0 = tri_v[:, 1, :] - tri_v[:, 2, :]
tri_v = tri_v[(dx_0[:, 0] != 0) + (dx_0[:, 1] != 0)]
dx_1 = tri_v[:, 0, :] - tri_v[:, 2, :]
tri_v = tri_v[(dx_1[:, 0] != 0) + (dx_1[:, 1] != 0)]
dx_2 = tri_v[:, 0, :] - tri_v[:, 1, :]
tri_v = tri_v[(dx_2[:, 0] != 0) + (dx_2[:, 1] != 0)]


A_v = np.concatenate((tri_v[:, :, 0:2], np.ones((tri_v.shape[0], 3, 1), )), axis=2)
tri_v = tri_v[np.linalg.det(A_v) != 0]
A_v = A_v[np.linalg.det(A_v) != 0]
b_v = tri_v[:, :, 2]
solve_v = np.linalg.solve(A_v, b_v).reshape(-1, 1, 3)

dx_0 = tri_v[:, 1, :] - tri_v[:, 2, :]
dx_1 = tri_v[:, 0, :] - tri_v[:, 2, :]
dx_2 = tri_v[:, 0, :] - tri_v[:, 1, :]

normal = np.cross(dx_0, dx_1)
norm = np.linalg.norm(normal, 2, axis=1)
normal /= norm.reshape(-1, 1)
normal[normal[:, 2] < 0] *= -1
normal.shape = [-1, 1, 3]

dx_0[dx_0[:, 1] == 0] = 1
dx_1[dx_1[:, 1] == 0] = 1
dx_2[dx_2[:, 1] == 0] = 1
dx_0 /= dx_0[:, 1].reshape(-1, 1)
dx_1 /= dx_1[:, 1].reshape(-1, 1)
dx_2 /= dx_2[:, 1].reshape(-1, 1)
dx = np.concatenate((dx_0[:, 0], dx_1[:, 0], dx_2[:, 0])).reshape(3, 1, -1).T

tri_v = np.concatenate((tri_v, dx, solve_v, normal), axis=1)

print(tri_v.shape)
for i in range(int(max(vertex[:, 1])), -1, -1):
    tran = tri_v[:, 0, 1] == i
    act_v = np.append(act_v, tri_v[tran]).reshape(-1, 6, 3)
    act_v = act_v[act_v[:, 2, 1] <= i]
    if np.size(act_v) == 0:
        continue
    act_v1 = act_v[act_v[:, 1, 1] < i]
    act_v2 = act_v[act_v[:, 1, 1] >= i]
    j_10 = (i - act_v2[:, 0, 1]) * act_v2[:, 3, 1] + act_v2[:, 0, 0]
    j_0 = (i - act_v2[:, 2, 1]) * act_v2[:, 3, 0] + act_v2[:, 2, 0]
    j_12 = (i - act_v1[:, 0, 1]) * act_v1[:, 3, 1] + act_v1[:, 0, 0]
    j_2 = (i - act_v1[:, 0, 1]) * act_v1[:, 3, 2] + act_v1[:, 0, 0]
    J = np.concatenate((j_10, j_12, j_0, j_2)).reshape(2, -1).T
    J = np.sort(J)
    J = np.ceil(J)

    for j in range(int(min(J[:, 0])), int(max(J[:, 1]))):
        tran = (J[:, 0] <= j) * (J[:, 1] > j)
        z = np.dot(act_v[tran][:, 4], [j, i, 1])
        if z.size == 0:
            continue
        draw_v = act_v[tran][np.argmax(z)]
        point_pos = np.array([j, i, max(z)])
        lp_vector = light_pos - point_pos
        lp_vector /= np.linalg.norm(lp_vector)
        diff = np.dot(lp_vector, draw_v[5])
        diffuse = diff * light_color
        pixels[i, j] = diffuse * object_color

elapsed = time.time() - start
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
