from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import read


source = '/home/x/xgit/zbuffer/model/wolf.obj'
r = read.Read(source)
v,f,x = r.out()

def drawFunc():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #glRotete(45, 0, 1,0)

    #线框消隐
    #glColorMask(0,0,0,0) 
    #glEnable(GL_DEPTH_TEST)
    #glDepthFunc(GL_LESS)
    #glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    #glPolygonOffset(1.1, 4.0)
    #glEnable(GL_POLYGON_OFFSET_FILL)
    #glBegin(GL_TRIANGLES)
    #for n in f:
    #    glColor3f(1.0,1.0,0.0)
    #    glVertex3fv(v[n[0]-1])
    #    glVertex3fv(v[n[1]-1])
    #    glVertex3fv(v[n[2]-1])
    #glEnd()
    #glDisable(GL_POLYGON_OFFSET_FILL)
    #glColorMask(1,1,1,1)
    
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE) 
    #glPointSize(5.0)
    glBegin(GL_TRIANGLES)
    for n in f:
        glColor3f(1.0,1.0,0.0)
        glVertex3fv(v[n[0]-1])
        glVertex3fv(v[n[1]-1])
        glVertex3fv(v[n[2]-1])
    glEnd()

    glFlush()

glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA | GLUT_DEPTH)
glutInitWindowSize(800,800)
glutCreateWindow("First")
glutDisplayFunc(drawFunc)
#glutIdleFunc(drawFunc)
glutMainLoop()
