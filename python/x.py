from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
from OpenGL.GL import shaders
import numpy as np
import read


class test(object):

    def __init__():
        pass

    source = '/home/x/xgit/zbuffer/model/wolf.obj'
    r = read.Read(source)
    vertex, face,x = r.out()
    vertex = sum(vertex,[])
    vertex = np.array(vertex)
    vertex = [[0.5, 0.5, 0], [-0.5, 0.5, 0], [0.5, -0.5, 0], [-0.5, -0.5, 0]]
    vertexbuffer = glGenBuffers(1)
    vbo = None
    shader = None
    def keyboard(key, foo, bar):
        exit()

    def Oninit():
        VERTEX_SHADER = shaders.compileShader(
                '''#version 120
                void main(){
                    gl_Position = gl_ModeViewProjectionMatrix * gl_Vertex;
                }''', GL_VERTEX_SHADER)

        FRAGMENT_SHADER = shaders.compileShader(
                """#version 120
                void main() {
                    gl_FragColor = vec4( 0, 1, 0, 1 );
                }""", GL_FRAGMENT_SHADER)

        shader = shaders.compileProgram(VERTEX_SHADER,FRAGMENT_SHADER)

        vbo = vbo.VBO(array(self.vertex, 'f'))
        
    def initgl():
        glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer)
        glBufferData(GL_ARRAY_BUFFER,vertex,GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def display():
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        
        glUseProgram(self.shader)
        vbo.bind()

        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf(self.vbo)
        glDrawArrays(GL_POINTS, 0, 4)
        vbo.unbind()
        glDisableClientState(GL_VERTEX_ARRAY)
        glUseProgram(0)

        glutSwapBuffers()

    glutInit()
    glutInitWindowPosition(200, 84)
    glutInitDisplayMode(GLUT_DOUBLE| GLUT_RGBA)
    glutInitWindowSize(800, 800)
    glutCreateWindow("x")
    Oninit()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMainLoop()

if __name__ == "__main__":
    test()
