from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import os
import time
import re


def read(path):

    def is_f(x):
        return x[0] == 'f'

    def is_v(x):
        if x[0] == 'v':
            if x[1] == ' ':
                return True
            return False

    open_file = open(path, 'r')
    read_file = open_file.readlines()

    list_f = filter(is_f, read_file)
    list_v = filter(is_v, read_file)

    obj_indices = []
    for n in list_f:
        obj_indices.append(list(x - 1 for x in map(int, re.split(r'[/\s]', n)[1:7:2])))
    obj_indices = np.array(obj_indices)

    obj_vertex = []
    for n in list_v:
        obj_vertex.append(list(map(float, re.split(r'\s', n)[1:4])))
    obj_vertex = np.array(obj_vertex)

    return obj_vertex, obj_indices


height = 600
width = 800
start = time.time()
source = os.getcwd() + '/' + 'wolf.obj'
vertex, indices = read(source)
v_max = np.max(vertex, axis=0)
v_min = np.min(vertex, axis=0)
zoom = np.max((v_max - v_min)[0:2] / [width, height])
vertex -= v_min
vertex /= zoom

faces = vertex[indices]
act_faces = np.array([])
pixels = np.zeros((height, width, 3))

light_pos = np.array([width, height, max(vertex[:, 2])])
light_color = np.array([1, 1, 1])
object_color = np.array([0.7, 0.7, 0.7])


for i in range(faces.shape[0]):
    faces[i] = faces[i, np.argsort(faces[:, :, 1], axis=1)[i, ::-1]]

vector_12 = faces[:, 1, :] - faces[:, 2, :]
vector_02 = faces[:, 0, :] - faces[:, 2, :]
vector_01 = faces[:, 0, :] - faces[:, 1, :]
normal = np.cross(vector_12, vector_02)
normal /= np.linalg.norm(normal, 2, axis=1).reshape(-1, 1)
normal[normal[:, 2] < 0] *= -1
normal.shape = [-1, 1, 3]

vector_12[vector_12[:, 1] == 0] = 1
vector_01[vector_01[:, 1] == 0] = 1
vector_12 /= vector_12[:, 1].reshape(-1, 1)
vector_02 /= vector_02[:, 1].reshape(-1, 1)
vector_01 /= vector_01[:, 1].reshape(-1, 1)
vector = np.concatenate((vector_12[:, 0], vector_02[:, 0], vector_01[:, 0])).reshape(3, 1, -1).T


A_faces = np.concatenate((faces[:, 0:3, 0:2], np.ones((faces.shape[0], 3, 1),)), axis=2)
b_faces = faces[:, 0:3, 2]
solve_faces = np.linalg.solve(A_faces, b_faces).reshape(-1, 1, 3)

faces = np.concatenate((faces, vector, solve_faces, normal), axis=1)

for i in range(int(max(vertex[:, 1])), -1, -1):
    tran = (faces[:, 0, 1] > i) * (faces[:, 0, 1] < i + 1)
    act_faces = np.append(act_faces, faces[tran]).reshape(-1, 6, 3)
    act_faces = act_faces[act_faces[:, 2, 1] < i]
    if np.size(act_faces) == 0:
        continue
    act_faces1 = act_faces[act_faces[:, 1, 1] < i]
    act_faces2 = act_faces[act_faces[:, 1, 1] >= i]
    act_faces = np.concatenate((act_faces2, act_faces1), axis=0)
    j_10 = (i - act_faces2[:, 0, 1]) * act_faces2[:, 3, 1] + act_faces2[:, 0, 0]
    j_0 = (i - act_faces2[:, 2, 1]) * act_faces2[:, 3, 0] + act_faces2[:, 2, 0]
    j_12 = (i - act_faces1[:, 0, 1]) * act_faces1[:, 3, 1] + act_faces1[:, 0, 0]
    j_2 = (i - act_faces1[:, 0, 1]) * act_faces1[:, 3, 2] + act_faces1[:, 0, 0]
    J = np.ceil(np.sort(np.concatenate((j_10, j_12, j_0, j_2)).reshape(2, -1).T))

    for j in range(int(min(J[:, 0])), int(max(J[:, 1]))):
        tran = (J[:, 0] <= j) * (J[:, 1] > j)
        z = np.dot(act_faces[tran][:, 4], [j, i, 1])
        if z.size == 0:
            continue
        draw_v = act_faces[tran][np.argmax(z)]
        point_pos = np.array([j, i, max(z)])
        lp_vector = light_pos - point_pos
        lp_vector /= np.linalg.norm(lp_vector)
        diff = np.dot(lp_vector, draw_v[5])
        diffuse = diff * light_color + 0.2
        pixels[i, j] = diffuse * object_color

elapsed = time.time() - start
print(elapsed)


def display():

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
