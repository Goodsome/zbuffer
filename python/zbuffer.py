from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import os
import re


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
    """扫描线zbuffer消隐算法"""
    source = os.getcwd() + '/' + 'wolf.obj'     # obj文件路径
    vertex, indices = read(source)

    v_max = np.max(vertex, axis=0)
    v_min = np.min(vertex, axis=0)
    zoom = np.max((v_max - v_min)[0:2] / [width, height])
    vertex -= v_min
    vertex /= zoom                              # 调整模型坐标以适应窗口

    faces = vertex[indices]                     # 模型的所有面
    act_faces = np.array([])                    # 扫描线激活的面
    pix = np.zeros((height, width, 3))          # 初始化像素

    light_pos = np.array([width, height, max(vertex[:, 2])])    # 光源位置
    light_color = np.array([1, 1, 1])                           # 光源颜色
    object_color = np.array([0.7, 0.7, 0.7])                    # 模型颜色

    for i in range(faces.shape[0]):                             # 调整面中点的顺序，以y降序排列
        faces[i] = faces[i, np.argsort(faces[:, :, 1], axis=1)[i, ::-1]]

    vector_12 = faces[:, 1, :] - faces[:, 2, :]
    vector_02 = faces[:, 0, :] - faces[:, 2, :]
    vector_01 = faces[:, 0, :] - faces[:, 1, :]
    normal = np.cross(vector_12, vector_02)
    normal /= np.linalg.norm(normal, 2, axis=1).reshape(-1, 1)
    normal[normal[:, 2] < 0] *= -1 
    normal.shape = [-1, 1, 3]                   # 计算每个面的法向量

    vector_12[vector_12[:, 1] == 0] = 1
    vector_01[vector_01[:, 1] == 0] = 1
    vector_12 /= vector_12[:, 1].reshape(-1, 1)
    vector_02 /= vector_02[:, 1].reshape(-1, 1)
    vector_01 /= vector_01[:, 1].reshape(-1, 1)
    vector = np.concatenate((vector_12[:, 0], vector_02[:, 0], vector_01[:, 0])).reshape(3, 1, -1).T    # 计算每条边的斜率

    a_faces = np.concatenate((faces[:, 0:3, 0:2], np.ones((faces.shape[0], 3, 1),)), axis=2)
    b_faces = faces[:, 0:3, 2]
    solve_faces = np.linalg.solve(a_faces, b_faces).reshape(-1, 1, 3)       # 计算每个面所在方程的系数：z = ax + by + c

    faces = np.concatenate((faces, vector, solve_faces, normal), axis=1)    # 将上述数据都加到面数组中

    for i in range(int(max(vertex[:, 1])), -1, -1):
        tran = (faces[:, 0, 1] >= i) * (faces[:, 0, 1] < i + 1)
        act_faces = np.append(act_faces, faces[tran])       # 当扫描线跨过三角形最上面的顶点，将面数据加入到活化面中
        act_faces.shape = [-1, 6, 3]
        act_faces = act_faces[act_faces[:, 2, 1] < i]       # 当扫描线离开三角形，在激活面数组中去除这个面的数据
        if np.size(act_faces) == 0:
            continue
        act_faces1 = act_faces[act_faces[:, 1, 1] < i]      # 扫描线在上半个三角形中
        act_faces2 = act_faces[act_faces[:, 1, 1] >= i]     # 扫描线在下半个三角形中
        act_faces = np.concatenate((act_faces2, act_faces1), axis=0)
        line_10 = (i - act_faces2[:, 0, 1]) * act_faces2[:, 3, 1] + act_faces2[:, 0, 0]
        line_0 = (i - act_faces2[:, 2, 1]) * act_faces2[:, 3, 0] + act_faces2[:, 2, 0]
        line_12 = (i - act_faces1[:, 0, 1]) * act_faces1[:, 3, 1] + act_faces1[:, 0, 0]
        line_2 = (i - act_faces1[:, 0, 1]) * act_faces1[:, 3, 2] + act_faces1[:, 0, 0]
        line = np.concatenate((line_10, line_12, line_0, line_2)).reshape(2, -1).T
        line = np.ceil(np.sort(line))           # 计算扫描线与边的交点

        for j in range(int(min(line[:, 0])), int(max(line[:, 1]))):
            tran = (line[:, 0] <= j) * (line[:, 1] > j)
            zbuffer = np.dot(act_faces[tran][:, 4], [j, i, 1])      # 计算zbuffer
            if zbuffer.size == 0:
                continue
            draw_faces = act_faces[tran][np.argmax(zbuffer)]        # 取zbuffer最大值的那个面
            point_pos = np.array([j, i, max(zbuffer)])
            lp_vector = light_pos - point_pos
            lp_vector /= np.linalg.norm(lp_vector)
            diff = np.dot(lp_vector, draw_faces[5])
            diffuse = diff * light_color + 0.2                      # 计算漫反射光 + 环境光
            pix[i, j] = diffuse * object_color                      # 写入像素值

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
main()
