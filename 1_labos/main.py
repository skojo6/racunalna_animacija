import pywavefront as pwf
import numpy as np
import math
import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time


def load_object():
    n_vertices = 0
    vertices = np.array([[0, 0, 0]])
    poly = np.array([[0, 0, 0]])
    with open('f16.obj', 'r', encoding='utf-8-sig') as dat:
        for line in dat:
            if line.startswith('v'):
                line_split = line.split()
                temp = []
                for i in line_split[1:]:
                    temp.append(float(i))
                vertices = np.append(vertices, [temp], axis=0)
                n_vertices += 1

            if line.startswith('f'):
                line_split = line.split()
                temp = []
                for i in line_split[1:]:
                    temp.append(int(i))
                poly = np.append(poly, [temp], axis=0)

        vertices = np.delete(vertices, 0, axis=0)
        poly = np.delete(poly, 0, axis=0)

    return vertices, poly


def load_curve():
    curve = pwf.Wavefront('spirala.obj')
    # tocke aproksimacijske uniformne B-splajn krivulje
    return curve


def animation_parameters(curve):
    vertices = curve.vertices
    n = len(vertices)
    n_segments = n-3

    # matrica B
    B = np.array([[-1, 3, -3, 1],
                  [3, -6, 3, 0],
                  [-3, 0, 3, 0],
                  [1, 4, 1, 0]])

    Bd = np.array([[-1, 3, -3, 1],
                   [2, -4, 2, 0],
                   [-1, 0, 1, 0]])

    p = []
    pd = []
    angles = []
    axis = []

    # pocetna orijentacija
    s = np.array([0, 0, 1])

    # segmenati krivulje
    for i in range(0, n_segments):
        # 4 kontrolne tocke objekta
        r = np.array(vertices[i:i+4])

        for t in np.arange(0, 1, 0.01):
            # racunanje tocaka segmenata krivulje (putanja)
            T = np.array([t**3, t**2, t, 1])
            temp = (T * (1/6)).dot(B)
            # putanja objekta
            pt = temp.dot(r)
            p.append(pt)

            # racunanje smjera tangente krivulje
            T = np.array([t**2, t, 1])
            temp = (T * (1/2)).dot(Bd)
            # ciljna orijentacija
            e = temp.dot(r)
            pd.append(e)

            # os rotacije
            axis.append(np.cross(s, e))

            # kut rotacije
            cos = s.dot(e) / (np.linalg.norm(s)*np.linalg.norm(e))
            acos = np.arccos(cos)
            angles.append(math.degrees(acos))

            s = pt + e

    return p, pd, angles, axis, n_segments


def draw():
    curve = load_curve()
    vertices, poly = load_object()
    p, pd, angles, axis, n_segments = animation_parameters(curve)

    n = len(p)

    t = 0
    counter = 0
    while True:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0.4, 0.2, 1, 0, 0, 0, 0, 1, 0)

        draw_curve(p)
        draw_object(vertices, poly, p, axis, angles, t)
        if counter % 50 == 0:
            draw_tangents(p, pd, t)
        counter += 1

        t += 1
        if t == n:
            t = 0
        glFlush()


def draw_curve(p):
    n = len(p)

    glPushMatrix()
    glBegin(GL_LINE_STRIP)
    for i in range(n):
        glVertex3f(p[i][0]/50, p[i][1]/50, p[i][2]/50)
    glEnd()
    glPopMatrix()


def draw_object(vertices, poly, p, axis, angles, t):
    glPushMatrix()
    glTranslatef(p[t][0]/50, p[t][1]/50, p[t][2]/50)
    glRotatef(angles[t], axis[t][0], axis[t][1], axis[t][2])
    glBegin(GL_LINES)
    for p in poly:
        glVertex3f(vertices[p[0]-1][0]/10, vertices[p[0]-1][1]/10, vertices[p[0]-1][2]/10)
        glVertex3f(vertices[p[1]-1][0]/10, vertices[p[1]-1][1]/10, vertices[p[1]-1][2]/10)
        glVertex3f(vertices[p[2]-1][0]/10, vertices[p[2]-1][1]/10, vertices[p[2]-1][2]/10)
    glEnd()
    glPopMatrix()


def draw_tangents(p, pd, t):
    glPushMatrix()
    glBegin(GL_LINES)
    glVertex3fv(p[t]/50)
    glVertex3fv((p[t] + pd[t])/50)
    glEnd()
    glPopMatrix()


if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(1000, 1000)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow("OpenGL")
    glutDisplayFunc(draw)
    glutIdleFunc(draw)
    glutMainLoop()
