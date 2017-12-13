from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import read

source = '/home/x/xgit/zbuffer/model/wolf.obj'
r = read.Read(source)
v,f,x = r.out()
rotate = 0
def keyboard(key, foo, bar):
    exit()

def initGL(width, height):
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)

def ResizeGL(width, height):
    if height == 0:
        height = 1

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def drawFunc():
    global rotate

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(0.0, -0.5, -3)
    glRotatef(rotate, 0, 1, 0)

    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE) 
    #glPointSize(5.0)
    glBegin(GL_TRIANGLES)
    for n in f:
        glColor3f(1, 1, 0)
        glVertex3fv(v[n[0]])
        glVertex3fv(v[n[1]])
        glVertex3fv(v[n[2]])
    glEnd()

    rotate += 1
    #fbo = glGenFramebuffers(1)
    #glBindFramebuffer(GL_FRAMEBUFFER, fbo)

    #color = glGenRenderbuffers(1)
    #glBindRenderbuffer(GL_RENDERBUFFER, color)
    #glRenderbufferStorage(
    #        GL_RENDERBUFFER,
    #        GL_RGBA,
    #        800,
    #        800,
    #        )
    #glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_RENDERBUFFER, color)

    #glBindRenderbuffer(GL_RENDERBUFFER, 0)
    #glBindFramebuffer(GL_FRAMEBUFFER, 0)
    #print(glCheckFramebufferStatus(GL_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE)
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(800,800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("First")
    glutDisplayFunc(drawFunc)
    glutIdleFunc(drawFunc)
    glutReshapeFunc(ResizeGL)
    glutKeyboardFunc(keyboard)
    initGL(800, 800)
    glutMainLoop()

main()
