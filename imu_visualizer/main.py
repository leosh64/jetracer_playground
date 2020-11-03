#!/usr/bin/env python3

"""
Module for visualizing orientation from IMU as 3D cube
"""

import pygame
from pygame.locals import *

from madgwick_py.quaternion import Quaternion

from imuviz.updater import ImuUpdater
from imuviz.renderer import Renderer

sensor_mounting_orientation = Quaternion(
    0.5663839027321934,
    -0.8235899489864758,
    -0.020782544029915546,
    0.021839334191962816,
)


def main():
    pygame.init()
    pygame.display.set_mode((640, 480), OPENGL | DOUBLEBUF)
    pygame.display.set_caption("IMU Orientation Visualization")

    renderer = Renderer(640, 480)

    frames = 0
    ticks = pygame.time.get_ticks()

    imu_thread = ImuUpdater(init_state=sensor_mounting_orientation)

    while True:
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break

        quat = imu_thread.get_data()

        # compensate for mounting position
        renderer.draw(quat * sensor_mounting_orientation.conj())

        pygame.display.flip()
        pygame.time.wait(1)
        frames += 1

    print(
        "Average framerate: %d" % ((frames * 1000) / (pygame.time.get_ticks() - ticks))
    )

    pygame.quit()


if __name__ == "__main__":
    main()
