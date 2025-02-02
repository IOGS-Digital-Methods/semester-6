# -*- coding: utf-8 -*-
"""*complex_light.py* file.

LED Illuminance cartography
    Semester 6 project of ONIP (Numerical Tools for Physicians)

    Create complex light composed of different sources

.. note:: LEnsE - Institut d'Optique - version 1.0

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>

Creation : feb/2025
Modification : None
"""

import numpy as np
from matplotlib import pyplot as plt
import illumin_v2 as il

class RingSource:
    """
    Create a ring composed of N light sources.
    """

    def __init__(self, I0, delta, number_of_sources, radius, angle, x, y, z, rotation:float=0):
        """

        :param I0:  float, maximal light intensity
        :param delta:   float, half-angle of emission (in degree)
        :param number_of_sources: int, number of sources in the ring
        :param radius: float, radius of the ring - in meter
        :param angle: float, direction of each source compared to the .. of the ring
        :param x:   float, x position of the source - in meter
        :param y:   float, y position of the source - in meter
        :param z:   float, z position of the source - in meter
        :param rotation: float, rotation of the ring - in degree
        """
        self.I0 = I0
        self.delta_deg = delta
        self.number_of_sources = number_of_sources
        self.radius = radius
        self.angle = angle
        self.x, self.y, self.z = x, y, z
        self.rotation = np.radians(rotation)
        self.sources_list = []
        self._create_list_of_source()

    def __str__(self):
        str = f'RING (I0={self.I0} / delta={self.delta_deg} / N={self.number_of_sources})'
        for i in range(self.number_of_sources):
            str += f'\n\t ({i}) {self.sources_list[i]}'
        return str

    def _create_list_of_source(self):
        for i in range(self.number_of_sources):
            thetai_deg = 360*i/self.number_of_sources + self.rotation
            thetai = np.radians(thetai_deg)
            xi = self.radius * np.cos(thetai) + self.x
            yi = self.radius * np.sin(thetai) + self.y
            source = il.Source(self.I0, self.delta_deg, xi, yi, self.z, thetai_deg, self.angle)
            self.sources_list.append(source)

    def get_number_of_sources(self):
        """Get the number of sources"""
        return self.number_of_sources

    def get_source(self, index_source:int):
        """
        Get a source in the list.
        :param index_source: int, index of the source.
        :return: the selected source of light.
        """
        if index_source < len(self.sources_list):
            return self.sources_list[index_source]
        else:
            return -1

    def set_angle(self, angle:float):
        self.angle = angle
        for i in range(self.number_of_sources):
            thetai_deg = 360 * i / self.number_of_sources + self.rotation
            self.sources_list[i].set_direction(thetai_deg, self.angle)


if __name__ == '__main__':
    ring1 = RingSource(100, 60, 8, 1, 10, 2.5, 2.5, 1, rotation=0)
    print(ring1)

    w_plan = il.WorkingPlan(5, 5, 0.01)
    w_plan.add_complex_source(ring1)

    illu1 = w_plan.process_global_illumination()
    ring1.set_angle(25)
    illu2 = w_plan.process_global_illumination()

    fig, ax = plt.subplots(nrows=2, ncols=2)
    # First subplot (top-left)
    ax[0, 0].imshow(illu1)
    ax[0, 0].set_title('Angle = 0 deg')

    # Second subplot (top-right)
    ax[0, 1].imshow(illu2)
    ax[0, 1].set_title('Angle = 50 deg')

    # Third subplot (bottom-left)
    central_line = illu1[:,illu1.shape[0]//2]
    ax[1, 0].plot(central_line)
    ax[1, 0].set_title('Central Line')

    # Fourth subplot (bottom-right)
    central_line = illu2[:, illu2.shape[0] // 2]
    ax[1, 1].plot(central_line)
    ax[1, 1].set_title('Central Line')
    plt.tight_layout()
    plt.show()

