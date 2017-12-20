from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL import shaders
import numpy as np
import read

source = os.getcwd() + '/' + 'wolf.obj'
r = read.Read(source)
model_vertex, model_indices = r.out()

cube_vertex = [
    1, 1, 1,
    1, 1, -1,
    1, -1, 1,
    1, -1, -1,
    -1, 1, 1,
    -1, 1, -1,
    -1, -1, 1,
    -1, -1, -1
]
cube_indices = [
    0, 1, 2,
    1, 3, 2,
    0, 5, 1,
    0, 4, 5,
    0, 2, 6,
    0, 6, 4,
    4, 6, 7,
    4, 7, 5,
    2, 3, 7,
    2, 7, 6,
    5, 7, 3,
    5, 3, 1,
]
model_shader = None
light_shader = None
VBO = None
VAO = None
EBO = None
rotate = 0
cameraPos = [0, 2, 9]

vertex = np.array(cube_vertex, np.float32).reshape(1, -1)
indices = np.array(cube_indices, np.int32).reshape(1, -1)


def init_shader():

    global model_shader, light_shader

    vertex_shader = shaders.compileShader(
        """
        void main() { 
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex; 
        }""", GL_VERTEX_SHADER)

    fragment_shader = shaders.compileShader(
        """
        void main() { 
        float ambientStrength = 1.0;
        vec3 lightColor = vec3(1, 1, 1);
        vec3 objectColor = vec3(1, 0.5, 0.31);
        vec3 ambient = ambientStrength * lightColor;
        vec3 result = ambient * objectColor;
        gl_FragColor = vec4(result, 1);
        }
        """, GL_FRAGMENT_SHADER)

    light_fragment_shader = shaders.compileShader(
        """
        void main() { 
        gl_FragColor = vec4(1);
        }
        """, GL_FRAGMENT_SHADER)

    model_shader = shaders.compileProgram(vertex_shader, fragment_shader)
    light_shader = shaders.compileProgram(vertex_shader, light_fragment_shader)


def init_vao():

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


def keyboard(*args):
    if args[0]:     # == '\033':
        exit()
    if args[0] == '\167':
        cameraPos[2] -= 0.1
    if args[0] == '\163':
        cameraPos[2] += 0.1
    if args[0] == '\141':
        cameraPos[0] -= 0.1
    if args[0] == '\144':
        cameraPos[0] += 0.1


def init_gl(width, height):

    init_shader()
    init_vao()

    glClearColor(0, 0, 0, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def reshape(width, height):

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def display():

    global rotate, cameraPos

    glClear(GL_COLOR_BUFFER_BIT)

    glLoadIdentity()
    gluLookAt(
        cameraPos[0], cameraPos[1], cameraPos[2],  # eye-point
        cameraPos[0], cameraPos[1], 0,  # center-of-view
        0, 1, 0,  # up-vector
    )
    # # glRotatef(rotate, 0, 1, 0)

    glTranslatef(0, 0, -5)
    glUseProgram(model_shader)
    glBindVertexArray(VAO)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glDrawElements(GL_TRIANGLES, indices.shape[1], GL_UNSIGNED_INT, None)
    glBindVertexArray(0)
    glUseProgram(0)

    # glTranslatef(2, 0, -6)
    # glUseProgram(light_shader)
    # glBindVertexArray(VAO)
    # glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    # glDrawElements(GL_TRIANGLES, indices.shape[1], GL_UNSIGNED_INT, None)
    # glBindVertexArray(0)
    # glUseProgram(0)

    glutSwapBuffers()
    rotate += 1


def main():

    glutInit()
    glutInitWindowPosition(200, 84)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(800, 800)
    glutCreateWindow("x")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    init_gl(800, 800)
    glutMainLoop()


main()
