# -*- coding: utf-8 -*-
"""*illumin_v2.py* file.

LED Illuminance cartography
    Semester 6 project of ONIP (Numerical Tools for Physicians)

This project is based on this subject : 
 

This file is attached to engineer training lab works in photonics.
More about the LEnsE : https://lense.institutoptique.fr/

.. note:: LEnsE - Institut d'Optique - version 1.0

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>

Creation : feb/2025
Modification : None
"""

import numpy as np
from matplotlib import pyplot as plt


def display_2D_figure(z):
    plt.figure()
    plt.imshow(z, cmap='gray')
    plt.colorbar()
    plt.show()

def vector_magnitude(v):
    if len(v.shape) > 1:
        return np.linalg.norm(v, axis=2)
    else:
        return np.linalg.norm(v)

class Source:

    def __init__(self, I0, delta, x=0, y=0, z=1, theta=0, zeta=0):
        """

        :param I0:  float, maximal light intensity
        :param delta:   float, half-angle of emission (in degree)
        :param x:   float, x position of the source - in meter
        :param y:   float, y position of the source - in meter
        :param z:   float, z position of the source - in meter
        :param theta:   float, angle of emission (in degree)
        :param zeta:   float, angle of emission (in degree)
        """

        self.I0 = I0
        self.delta_deg = delta
        self.delta = np.radians(self.delta_deg)
        self.x, self.y, self.z, self.theta, self.zeta = x, y, z, np.radians(theta), np.radians(zeta + 90)

        # definition of ux, uy, uz = unitary vector of the main source direction
        self.ux = np.cos(self.theta)*np.cos(self.zeta)
        self.uy = np.sin(self.theta)*np.cos(self.zeta)
        self.uz = -np.sin(self.zeta)

    def _calculate_unitary_direction_vector(self):
        self.ux = np.cos(self.theta)*np.cos(self.zeta)
        self.uy = np.sin(self.theta)*np.cos(self.zeta)
        self.uz = -np.sin(self.zeta)

    def __str__(self):
        return f'LED (I0={self.I0} / delta={self.delta_deg}) [{self.x};{self.y};{self.z}]'

    def get_coords(self):
        return self.x, self.y, self.z

    def get_intensity_deg(self, angle):
        """
        Calculate light intensity of the source in a specific direction.
        :param angle:   float, angle in degree
        :return:
            value of the light intensity in the specific angle
        """
        return self.I0 * np.exp(-(4 * np.log(2)) * (angle / self.delta_deg) ** 2)

    def get_intensity_rad(self, alpha):
        """
        Calculate light intensity of the source in a specific direction.
        :param angle:   float, angle in radian
        :return:
            value of the light intensity in the specific angle
        """
        return self.I0 * np.exp(-(4 * np.log(2)) * (alpha / self.delta) ** 2)

    def get_direction_vector(self):
        """
        Direction vector of the source.
        """
        return self.ux, self.uy, self.uz

    def set_light(self, I0, delta):
        """
        Modify the light parameters
        :param I0:  float, maximal light intensity
        :param delta:   float, half-angle of emission (in degree)
        """
        self.I0 = I0
        self.delta = delta

    def set_position(self, x, y, z):
        """
        Modify the position of the source
        :param x:   float, x position of the source - in meter
        :param y:   float, y position of the source - in meter
        :param z:   float, z position of the source - in meter
        :param theta:   float, angle of emission (in degree)
        :param zeta:   float, angle of emission (in degree)
        """
        self.x, self.y, self.z = x, y, z

    def set_direction(self, theta, zeta):
        """
        Modify the direction of the source
        :param theta:   float, angle of emission (in degree)
        :param zeta:   float, angle of emission (in degree)
        """
        self.theta, self.zeta = np.radians(theta), np.radians(zeta + 90)
        self._calculate_unitary_direction_vector()


class WorkingPlan:
    """
    Working plan.
    Origin at x=0, y=0. Altitude of the plan z=0. Plan is horizontal.
    """

    def __init__(self, length, width, step):
        """

        :param width:   float, width of the screen (in meter)
        :param length:  float, length of the screen (in meter)
        :param step:    float, step of the screen grid
        """
        self.width = width
        self.length = length
        self.step = step
        self.nb_x_len = int(self.length / self.step + 1)
        self.x_len = np.linspace(0, self.length, self.nb_x_len)
        self.nb_y_width = int(self.width / self.step + 1)
        self.y_width = np.linspace(0, self.width, self.nb_y_width)
        self.mesh_y, self.mesh_x = np.meshgrid(self.y_width, self.x_len)
        # definition of wx, wy, wz = unitary vector of the plan - vertical in this case !
        self.wx, self.wy, self.wz = 0, 0, 1
        # List of the sources
        self.sources_list: Source = []
        self.complex_sources_list = []

    def get_direction_vector(self):
        """
        Direction vector of the plan.
        """
        return self.wx, self.wy, self.wz

    def add_source(self, source):
        self.sources_list.append(source)

    def add_complex_source(self, source):
        self.complex_sources_list.append(source)

    def print_sources_list(self):
        for k in range(len(self.sources_list)):
            print(f'{k+1}: {self.sources_list[k]}')
        for k in range(len(self.complex_sources_list)):
            print(f'C{k+1}: {self.complex_sources_list[k]}')

    def process_plan_to_source_vector(self, source:Source):
        """
        Calculate the plan to source vector - from a point of the plan.
        :param source: light source.
        :return: 2D array (size of the plan) with the value of the PS vector.
        """
        # PS vector = xP-xS, yP-yS, zP-zS
        source_x, source_y, source_z = source.get_coords()
        ps_vect_x = self.mesh_x-source_x
        ps_vect_y = self.mesh_y-source_y
        ps_vect_z = np.zeros_like(ps_vect_x)
        ps_vect_z[:,:] = -source_z
        ps_vect = np.stack((ps_vect_x, ps_vect_y, ps_vect_z), axis=-1)
        return ps_vect

    def process_alpha_source(self, source:Source, ps_vect: np.ndarray=[]):
        """
        Calculate alpha angle for each point of the working plan.
        :param source: light source.
        :param ps_vect: point to source vector.
        :return: 2D array (size of the plan) with the value of the angle alpha.
        """
        if len(ps_vect) == 0:
            ps_vect = self.process_plan_to_source_vector(source)
        # direction vector of the source
        ns = np.stack(source.get_direction_vector(), axis=-1)
        # Alpha angle
        ps_mag = vector_magnitude(ps_vect)
        ns_mag = vector_magnitude(ns)   # equal to 1
        cos_alpha = np.dot(ps_vect, ns)/(ps_mag*ns_mag)
        return np.arccos(cos_alpha)

    def get_intensity_led(self, source:Source, alpha: np.ndarray=[]):
        """
        Calculate intensity of a source for each point of the working plan.
        :param source: light source.
        :param alpha: Array of alpha angles.
        :return: 2D array (size of the plan) with the value of the intensity of the source.
        """
        if len(alpha) == 0:
            alpha = self.process_alpha_source(source)
        return source.get_intensity_rad(alpha)

    def process_cospsi_source(self, source:Source, ps_vect: np.ndarray=[]):
        """
        Calculate psi angle for each point of the working plan.
        :param source: light source.
        :param ps_vect: point to source vector.
        :return: 2D array (size of the plan) with the value of the angle psi.
        """
        if len(ps_vect) == 0:
            ps_vect = self.process_plan_to_source_vector(source)
        # direction vector of the plan
        nplan = np.stack((self.get_direction_vector()), axis=-1)
        # Psi angle
        ps_mag = vector_magnitude(ps_vect)
        np_mag = vector_magnitude(nplan)   # equal to 1
        cos_psi = np.dot(ps_vect, nplan)/(ps_mag*np_mag)
        return cos_psi, ps_mag

    def get_illumination_source(self, source:Source, ps_mag:np.ndarray,
                                intensity: np.ndarray=[], cospsi: np.ndarray=[]):
        """
        Calculate illumination of a source for each point of the working plan.
        :param source: light source.
        :param intensity: Intensity for each point of the plan.
        :param psi: Psi angle for each point of the plan.
        :return: 2D array (size of the plan) with the value of the intensity of the source.
        """
        if len(intensity) == 0:
            intensity = self.get_intensity_led(source)
        if len(cospsi) == 0:
            psi, ps_mag = self.process_psi_source(source)
        return -intensity*cospsi / ps_mag**2


    def process_global_illumination(self):
        """"""
        global_illumination = []
        # Simple sources
        nb_source = len(self.sources_list)
        for k in range(nb_source):
            source = self.sources_list[k]
            print(f'Source {k}')
            ps_vect = self.process_plan_to_source_vector(source)
            alpha = self.process_alpha_source(source, ps_vect)
            intensity = self.get_intensity_led(source, alpha)
            cos_psi, ps_mag = self.process_cospsi_source(source, ps_vect)
            illumine = self.get_illumination_source(source, ps_mag, intensity, cos_psi)
            if k == 0:
                global_illumination = illumine
            else:
                global_illumination += illumine
        # Complex sources
        nb_source = len(self.complex_sources_list)
        for k in range(nb_source):
            print(f'C Source {k}')
            nb = self.complex_sources_list[k].get_number_of_sources()
            print(f'Nb = {nb}')
            for m in range(self.complex_sources_list[k].get_number_of_sources()):
                source = self.complex_sources_list[k].get_source(m)
                ps_vect = self.process_plan_to_source_vector(source)
                alpha = self.process_alpha_source(source, ps_vect)
                intensity = self.get_intensity_led(source, alpha)
                cos_psi, ps_mag = self.process_cospsi_source(source, ps_vect)
                illumine = self.get_illumination_source(source, ps_mag, intensity, cos_psi)
                if len(global_illumination) == 0:
                    global_illumination = illumine
                else:
                    global_illumination += illumine
        return global_illumination


if __name__ == '__main__':
    led1 = Source(100, 30, 1, 1.5, 1, 0, 0)
    led1.set_direction(120, 50)
    led2 = Source(100, 10, 1.5, 2.5, 1, 90, 50)

    w_plan = WorkingPlan(2, 3, 0.1)
    w_plan.add_source(led1)
    #w_plan.add_source(led2)
    w_plan.print_sources_list()

    # TO MOVE !
    illu = w_plan.process_global_illumination()
    display_2D_figure(illu)
