from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

pixels = np.random.random((800, 600, 3))
for i in range(800):
    for j in range(600):
        if i < 400:
            pixels[i][j] = [1.0, 0.0, 0.0]
        else:
            pixels[i][j] = [0.0 ,1.0, 0.0]

def display():
    global pixels

    glClear(GL_COLOR_BUFFER_BIT)
   
    glDrawPixels(800, 600, GL_RGB, GL_FLOAT, pixels)
    glutSwapBuffers()

def keyboard(*args):
    if args:
        exit()

def initGL():

    glClearColor(0, 0, 0, 0)

def main():

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(800, 600)
    glutCreateWindow("Draw Pixels")
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    initGL()
    glutMainLoop()

main()
