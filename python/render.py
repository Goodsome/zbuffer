from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL import shaders
import numpy as np
import read
import os

source = os.getcwd() + '/' + 'wolf.obj'
r = read.Read(source)
vertex_data, indices_data = r.out()

shaderProgram = None
VBO = None
VAO = None
EBO = None

vertex = np.array(vertex_data, np.float32)
indices = np.array(indices_data, np.int32)


def keyboard(*args):
    exit()


def init_gl():

    init_shader()
    init_vbo_vao()


def init_shader():

    global shaderProgram

    vertex_shader = shaders.compileShader(
        """
        void main() {
            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex; 
        }""", GL_VERTEX_SHADER)

    fragment_shader = shaders.compileShader(
        """
        void main() {
            gl_FragColor = vec4( 1, 1, 0, 1 ); 
            }""", GL_FRAGMENT_SHADER)

    shaderProgram = shaders.compileProgram(vertex_shader, fragment_shader)


def init_vbo_vao():

    global vertex, VAO, VBO, EBO

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)

    glBufferData(GL_ARRAY_BUFFER, vertex, GL_STATIC_DRAW)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    glBindVertexArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)


def reshape(width, height):

    glViewport(0, 0, width, height)


def display():
    glClearColor(0.2, 0.3, 0.3, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(shaderProgram)
    glBindVertexArray(VAO)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glDrawElements(GL_TRIANGLES, 3 * indices.shape[0], GL_UNSIGNED_INT, None)
    glBindVertexArray(0)
    glUseProgram(0)

    glFlush()


def main():

    glutInit()
    glutInitWindowPosition(200, 84)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutInitWindowSize(800, 800)
    glutCreateWindow("x")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    init_gl()
    glutMainLoop()


main()

