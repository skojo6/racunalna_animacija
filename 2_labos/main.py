import pywavefront as pwf
import numpy as np
import math
import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import random


life_limit = 5
number_of_particles = 100
rgb1 = [255, 0, 0]
rgb2 = [255, 247, 0]
rgb3 = [160, 160, 160]
particles = []
not_first = True


def draw_particles():
    for i in range(number_of_particles):  # first particles
        list = []
        x = random.uniform(-1, 1)/10
        y = random.uniform(-1, 1)/10
        z = random.uniform(-1, 1)/10
        life = random.randint(1, 4)

        list.append(x)
        list.append(y)
        list.append(z)
        list.append(life)
        particles.append(list)

    while True:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        draw_particle(particles)

        for particle in particles:
            if particle[3] > life_limit:
                particles.remove(particle)

                # create new particle
                list_new = []
                x_new = random.uniform(-1, 1)/10
                y_new = random.uniform(-1, 1)/10
                z_new = random.uniform(-1, 1)/10
                life_new = random.randint(1, 4)

                list_new.append(x_new)
                list_new.append(y_new)
                list_new.append(z_new)
                list_new.append(life_new)

                particles.append(list_new)

        time.sleep(1)

        for particle in particles:
            # moving particles
            x = random.uniform(-0.5, 0.5)/10
            y = random.uniform(-0.5, 0.5)/10
            z = random.uniform(-0.5, 0.5)/10

            particle[0] += x
            particle[1] += y
            particle[2] += z
            particle[3] += 1

        glFlush()


def draw_particle(ps):
    glPushMatrix()
    glPointSize(6)
    glBegin(GL_POINTS)
    for particle in ps:
        if particle[3] == 1 or particle[3] == 2:
            glColor3f(rgb1[0], rgb1[1], rgb1[2])
        if particle[3] == 3 or particle[3] == 4:
            glColor3f(rgb2[0], rgb2[1], rgb2[2])
        if particle[3] == 5:
            glColor3f(rgb3[0], rgb3[1], rgb3[2])
        glVertex3f(particle[0], particle[1], particle[2])
    glEnd()
    glPopMatrix()


def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -100)
    draw_particles()
    glutSwapBuffers()


if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_RGB)
    glutInitWindowSize(1000, 1000)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow("OpenGL")
    glutDisplayFunc(draw)
    glutIdleFunc(draw)
    glutMainLoop()
