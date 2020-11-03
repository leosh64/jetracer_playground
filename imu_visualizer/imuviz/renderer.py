import math

import pygame.font
import pygame.image

from OpenGL.GL import *
from OpenGL.GLU import *


class Renderer:
    """OpenGL rendering and text drawing

    Sets up OpenGL for rendering of the cube and provides
    functions for drawing the cube given a quaternion as well
    as text
    """

    def __init__(self, window_width, window_height):
        """Initialize OpenGL renderer

        Args:
            window_width (int): Window width in pixels
            window_height (int): Window height in pixels
        """
        glShadeModel(GL_SMOOTH)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        # glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

        glViewport(0, 0, window_width, window_height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1.0 * window_width / window_height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # map for buffering fonts
        self.fonts = {}

        cube_length = 1.0
        cube_width = 0.6
        cube_height = 0.2

        self.vertices = (
            (cube_length, cube_height, cube_width),
            (cube_length, cube_height, -cube_width),
            (cube_length, -cube_height, -cube_width),
            (cube_length, -cube_height, cube_width),
            (-cube_length, cube_height, cube_width),
            (-cube_length, -cube_height, -cube_width),
            (-cube_length, -cube_height, cube_width),
            (-cube_length, cube_height, -cube_width),
        )
        self.quads = (
            (0, 3, 6, 4),
            (2, 5, 6, 3),
            (1, 2, 5, 7),
            (1, 0, 4, 7),
            (7, 4, 6, 5),
            (2, 3, 0, 1),
        )
        self.colors = (
            (0.0, 1.0, 0.0),
            (1.0, 0.5, 0.0),
            (1.0, 0.0, 0.0),
            (1.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
            (1.0, 0.0, 1.0),
        )

    def draw(self, quaternion):
        """Draw cube according to quaternion rotation

        Args:
            quaternion (madgwick_py.quaternion): Quaternion to draw
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0, 0.0, -7.0)

        self.draw_text(
            (-2.6, 1.8, 2), "Orientation from IMU filtered by MadgwickAHRS", 18,
        )
        self.draw_text((-2.6, -2, 2), "Press ESC to exit.", 16)

        w = quaternion[0]
        nx = quaternion[1]
        ny = quaternion[2]
        nz = quaternion[3]

        [roll, pitch, yaw] = quaternion.to_euler_angles()
        self.draw_text(
            (-2.6, -1.8, 2),
            "Yaw: %f, Pitch: %f, Roll: %f"
            % (math.degrees(yaw), math.degrees(pitch), math.degrees(roll)),
            16,
        )
        glRotatef(2 * math.degrees(math.acos(w)), -1 * nx, nz, ny)

        glBegin(GL_QUADS)

        for quad, color in zip(self.quads, self.colors):
            glColor3fv(color)
            for vertex in quad:
                glVertex3fv(self.vertices[vertex])

        glEnd()

    def get_font(self, size):
        """Get font for specified size

        If the font size doesn't exist in the buffer, it will be created.

        Args:
            size (int): Font size in pt

        Returns:
            pygame.Font: pygame Font object
        """
        if size not in self.fonts:
            self.fonts[size] = pygame.font.SysFont("Courier", size, True)

        return self.fonts[size]

    def draw_text(self, position, text, size):
        """Draw text on screen

        Args:
            position (tuple(int, int, int)): 3D position of the text
            text (string): String to display
            size (int): Font size in pt
        """
        font = self.get_font(size)

        surface = font.render(text, True, (255, 255, 255, 255), (0, 0, 0, 255))
        text_data = pygame.image.tostring(surface, "RGBA", True)
        glRasterPos3d(*position)
        glDrawPixels(
            surface.get_width(),
            surface.get_height(),
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            text_data,
        )
