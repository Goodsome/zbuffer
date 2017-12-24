from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import os
import re
import time

def read(path):
    """读取文件数据，输出顶点数据以及面索引数据"""

    def is_f(x):
        return x[0] == 'f'

    def is_v(x):
        if x[0] == 'v':
            if x[1] == ' ':
                return True
            return False

    open_file = open(path, 'r')
    read_file = open_file.readlines()

    list_f = filter(is_f, read_file)            # 提取f开头的数据，为面索引
    list_v = filter(is_v, read_file)            # 提取v开头的数据，为顶点数据

    obj_indices = []
    for n in list_f:
        obj_indices.append(list(x - 1 for x in map(int, re.split(r'[/\s]', n)[1:7:2])))
    obj_indices = np.array(obj_indices)         # 整理数据格式为np.array

    obj_vertex = []
    for n in list_v:
        obj_vertex.append(list(map(float, re.split(r'\s', n)[1:4])))
    obj_vertex = np.array(obj_vertex)           # 整理数据格式为np.array

    return obj_vertex, obj_indices


def draw_pixels():
    source = os.getcwd() + '/' + 'wolf.obj'  # obj文件路径
    vertex, indices = read(source)

    v_max = np.max(vertex, axis=0)
    v_min = np.min(vertex, axis=0)
    zoom = np.max((v_max - v_min)[0:2] / [width, height])
    vertex -= v_min
    vertex /= zoom  # 调整模型坐标以适应窗口

    faces = vertex[indices]  # 模型的所有面
    act_faces = np.array([])  # 扫描线激活的面
    pix = np.zeros((height, width, 3))  # 初始化像素

    start = time.time()
    tri = faces
    a = np.array([[-1, 1, 0], [-1, 0, 1]])
    A = np.dot(a, tri)[:, 0:2]
    print(A)
    print(time.time() - start)

    return pix


def display():
    """显示回调函数"""
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT)
    glDrawPixels(width, height, GL_RGB, GL_FLOAT, pixels)
    glFlush()


def keyboard(*args):
    """键盘回调函数，按下任意键退出程序"""
    if args:
        exit()


def main():

    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutInitWindowSize(width, height)
    glutCreateWindow("Draw Pixels")
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMainLoop()


height = 600
width = 800
pixels = draw_pixels()
# main()
