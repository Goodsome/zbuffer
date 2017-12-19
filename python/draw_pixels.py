from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import read
import os

height = 600
width = 800

source = os.getcwd() + '/' + 'wolf.obj'
r = read.Read(source)
vertex, indices, faces = r.out()
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

for i in range(tri_v.shape[0]):
    tri_v[i] = tri_v[i, np.argsort(tri_v[:, :, 1], axis=1)[i, ::-1]]
tri_v = tri_v[np.argsort(tri_v[:, 0, 1])[::-1]]

for i in range(int(max(vertex[:, 1])), -1, -1):
    tran = (tri_v[:, 0, 1] > i) * (tri_v[:, 0, 1] < i + 1)
    act_v = np.append(act_v, tri_v[tran]).reshape(-1, 3, 3)
    act_v = act_v[act_v[:, 2, 1] < i]
    act_v1 = act_v[act_v[:, 1, 1] < i]
    act_v2 = act_v[act_v[:, 1, 1] > i]
    print(i)
    for j in range(int(np.min(act_v[:, :, 0])), int(np.max(act_v[:, :, 0])) + 1):
        # dx = (act_v1[:, 0, 0] - act_v1[:, 2, 0]) / (act_v1[:, 0, 1] - act_v1[:, 2, 1])
        # tran_l = np.ceil(dx * (i - act_v1[:, 0, 1]) + act_v1[:, 0, 0]) == j
        # act_l = np.append(act_l, act_v1[tran_l])
        pass

print(act_v.shape)


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

# main()
