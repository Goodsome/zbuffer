from OpenGL.GL import *
from OpenGL.GLU import *
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

v = vertex[indices]
colors = np.full(indices.shape, 0.07)
zbuffer = np.zeros(width)
pixels = np.zeros((height, width, 3))

a = v[:, :, 1]
b = np.argsort(a, axis=1)
for i in range(v.shape[0]):
    v[i] = v[i, b[i,::-1]]
c = v[:, 0, 1]
d = np.argsort(c)
v = v[d[::-1]]


def display():
    global pixels

    glClear(GL_COLOR_BUFFER_BIT)
   
    glDrawPixels(width, height, GL_RGB, GL_FLOAT, pixels)
    glutSwapBuffers()

def keyboard(*args):
    if args:
        exit()

def initGL():

    glClearColor(0, 0, 0, 0)

def main():

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(width, height)
    glutCreateWindow("Draw Pixels")
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    initGL()
    glutMainLoop()

# main()
