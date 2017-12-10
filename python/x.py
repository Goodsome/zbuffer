
m OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL import shaders
import numpy as np

shaderProgram = None
vertex_buffer = None
vertex_array = None
vertex_data = [0, 1, 0,
               -1, -1, 0,
               1, -1, 0, ]
vertex = np.array(vertex_data, np.float32)


def keyboard(key, foo, bar):
    exit()


def init_gl(width, height):

    # glMatrixMode(GL_PROJECTION)
    # glLoadIdentity()
    # gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
    # glMatrixMode(GL_MODELVIEW)

    init_shader()
    init_vbo_vao()

def init_shader():

    global shaderProgram

    VERTEX_SHADER = shaders.compileShader(
        """
        void main() {
            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex; 
        }""", GL_VERTEX_SHADER)

    FRAGMENT_SHADER = shaders.compileShader(
        """
        void main() {
            gl_FragColor = vec4( 0, 1, 0, 1 ); 
            }""", GL_FRAGMENT_SHADER)

    shaderProgram = shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)


def init_vbo_vao():

    global vertex, vertex_array, vertex_buffer

    vertex_buffer = glGenBuffers(1)
    vertex_array = glGenVertexArrays(1)

    glBindVertexArray(vertex_array)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, vertex, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)


def reshape(width, height):

    glViewport(0, 0, width, height)
    # glLoadIdentity()
    # gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
    # glMatrixMode(GL_MODELVIEW)


def display():
    glClearColor(0.2, 0.3, 0.3, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # glLoadIdentity()
    # glTranslatef(-1.5, 0.0, -7.0)

    glUseProgram(shaderProgram)
    glBindVertexArray(vertex_array)
    glDrawArrays(GL_TRIANGLES, 0, 3)

    glBindVertexArray(0)
    glUseProgram(0)

    glutSwapBuffers()


def main():
    glutInit()
    glutInitWindowPosition(200, 84)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(800, 800)
    glutCreateWindow("x")
    glutDisplayFunc(display)
    #glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    init_gl(800, 800)
    glutMainLoop()


main()

