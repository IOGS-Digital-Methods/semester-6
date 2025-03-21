"""
LED Illuminance cartography
    Semester 6 project of ONIP (Numerical Tools for Physicians)

Help at : https://www.hindawi.com/journals/mpe/2021/8099757/
"""

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import proj3d


class working_plan:
    def __init__(self, width, length, step):
        """

        :param width:   float, width of the screen (in meters)
        :param length:  float, length of the screen (in meters)
        :param step:    float, step of the screen grid
        """
        self.width = width
        self.length = length
        self.step = step
        self.nb_x_len = int(self.length / self.step + 1)
        self.x_len = np.linspace(0, self.length, self.nb_x_len)
        self.nb_y_width = int(self.width / self.step + 1)
        self.y_width = np.linspace(0, self.width, self.nb_y_width)
        self.sources_list = []

    def __str__(self):
        return f'Plan (L = {self.longueur} / l = {self.largeur}'

    def get_mesh(self):
        self.mesh_y, self.mesh_x = np.meshgrid(self.y_width, self.x_len)
        return self.mesh_x, self.mesh_y

    def add_source(self, source):
        self.sources_list.append(source)

    def print_sources_list(self):
        for k in range(len(self.sources_list)):
            print(f'{k+1}: {self.sources_list[k]}')

    def calculate_source_map(self, source):
        x_mesh, y_mesh = self.get_mesh()
        zout = np.sqrt(x_mesh ** 2 + y_mesh ** 2)

        dist_v, angle_v = self.get_angle_distance(x_mesh, y_mesh, 0, source)
        zout = source.led_illumination(dist_v, angle_v)
        return x_mesh, y_mesh, zout

    def get_x_y_vector(self):
        return self.x_len, self.y_width

    def get_angle_distance(self, x, y, z, source):
        x_s, y_s, z_s = source.get_coords()
        radius = (x_s - x)**2 + (y_s - y)**2 + (z_s - z)**2
        angle = 0
        angle = np.arctan(np.sqrt((x_s-x)**2 + (y_s-y)**2)/(z_s-z))
        return radius, angle

    def get_global_map(self):
        zz_f = np.zeros((len(self.x_len), len(self.y_width)))
        for k in range(len(self.sources_list)):
            xx, yy, zz = self.calculate_source_map(source=self.sources_list[k])
            zz_f += zz
        return xx, yy, zz_f

    def display_global_map(self):
        xx, yy, zz_f = self.get_global_map()
        plt.figure()
        h = plt.pcolormesh(yy, xx, zz_f)
        plt.colorbar()
        plt.show()

    def display_global_map_contour(self):
        xx, yy, zz_f = self.get_global_map()
        plt.figure()
        max_zz = np.max(zz_f)
        nb_levels = 20
        levels = np.linspace(0, max_zz, nb_levels)
        h = plt.contour(yy, xx, zz_f, levels=levels)
        plt.colorbar()
        plt.show()

    def display_working_space(self):
        x, y, z = [], [], []
        u, v, w = [], [], []
        for k in range(len(self.sources_list)):
            xx, yy, zz = self.sources_list[k].get_coords()
            x.append(xx)
            y.append(yy)
            z.append(zz)
            ux, vy, wz = self.sources_list[k].get_direction_vector()
            u.append(0.3*ux)
            v.append(0.3*vy)
            w.append(0.3*wz)

        fig = plt.figure()
        ax = plt.axes(projection='3d')  # Affichage en 3D
        ax.scatter(x, y, z, marker='d')
        ax.quiver(x, y, z, u, v, w)

        x_mesh, y_mesh = self.get_mesh()
        z = x_mesh*0 + y_mesh*0
        ax.plot_surface(x_mesh, y_mesh, z, alpha=0.5)

        # Print map in 2D...
        xx, yy, zz_f = self.get_global_map()
        max = np.max(zz_f)
        # cset = ax.contour(xx, yy, zz_f, zdir='z', offset=0.1)
        # ax.plot_surface(xx, yy, zz_f, alpha=0.3)

        plt.show()

class LED_source:

    def __init__(self, I0, delta, x=0, y=0, z=1, theta=0, zeta=0):
        '''

        :param I0:  float, maximal light intensity
        :param delta:   float, half-angle of emission (in degree)
        :param x:   float, x position of the source
        :param y:   float, y position of the source
        :param z:   float, z position of the source
        :param theta:   float, angle of emission (in degree)
        :param zeta:   float, angle of emission (in degree)
        '''
        self.I0 = I0
        self.delta_deg = delta
        self.delta = self.delta_deg*np.pi / 180

        self.x, self.y, self.z, self.theta, self.zeta = x, y, z, np.radians(theta), np.radians(zeta+90)
        # definition of ux, uy, uz = unitary vector of the main source direction
        self.ux = np.cos(self.theta)*np.cos(self.zeta)
        self.uy = np.sin(self.theta)*np.cos(self.zeta)
        self.uz = -np.sin(self.zeta)

        norm = (self.ux)**2 + (self.uy)**2 + (self.uz)**2
        print(norm)

    def __str__(self):
        return f'LED (I0={self.I0} / delta={self.delta_deg})'

    def led_intensity(self, angle):
        """
        indicatrice de rayonnement
        :param angle:   float, angle
        :return:
            value of the light intensity in the specific angle
        """
        return self.I0*np.exp(-(4*np.log(2))*(angle / self.delta)**2)

    def led_illumination(self, distance, angle):
        """

        :param distance:    float, distance between light source and the point of view (in meters)
        :param angle:   float, angle between normal vector of the light source and the point of view (in degrees)
        :return:
            illumination value at a specific distance and angle

        help from : https://fr.wikibooks.org/wiki/Photographie/Photom%C3%A9trie/Calculs_photom%C3%A9triques_usuels
        """
        angle_new = angle * np.pi / 180
        return self.led_intensity(angle) * np.cos(angle_new) / (distance**2)

    def get_coords(self):
        return self.x, self.y, self.z

    def get_params(self):
        return self.I0, self.zeta, self.theta

    def get_direction_vector(self):
        return self.ux, self.uy, self.uz

    def display_radiation_diagram(self):
        alpha = np.linspace(0, np.pi, 101)
        led_intens = self.led_intensity(alpha)
        plt.figure()
        plt.plot(alpha*180/np.pi, led_intens)
        plt.figure()
        plt.polar(alpha, led_intens)
        plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    led1 = LED_source(1, 30, x=0.5, y=1, z=2)
    led2 = LED_source(1, 20, x=0.2, y=0.2, z=0.5)
    led3 = LED_source(2, 90, x=0.8, y=1.8)

    # led1.display_radiation_diagram()

    # Plan 1
    '''
    wp = working_plan(2, 1, 0.001)

    wp.add_source(led1)
    wp.add_source(led2)
    wp.add_source(led3)
    wp.print_sources_list()

    grid_x, grid_y = wp.get_mesh()
    print(grid_x.shape)

    wp.display_global_map()

    wp.display_working_space()
    '''
    
    # Plan 2 - Simu 01
    wp0 = working_plan(2, 2, 0.001)
    led0 = LED_source(1, 30, x=1, theta=0, zeta=0, y=1, z=2)

    wp0.add_source(led0)
    wp0.display_global_map()
    wp0.display_global_map_contour()
    wp0.display_working_space()


    # Plan 2 - Simu 02
    wp = working_plan(2, 2, 0.001)
    led1 = LED_source(1, 30, x=1, theta=0, zeta=0, y=0.4, z=2)
    led1.display_radiation_diagram()
    angle_dif = 30*np.pi/180  # radians
    print(f'X={1 + 0.6 * np.cos(angle_dif)}')
    print(f'X={1 - 0.6 * np.cos(angle_dif)}')
    print(f'Y={1 + 0.6 * np.sin(angle_dif)}')
    led2 = LED_source(1, 30, x=1+0.6*np.cos(angle_dif), theta=0, zeta=0, y=1+0.6*np.sin(angle_dif), z=2)
    led3 = LED_source(1, 30, x=1-0.6*np.cos(angle_dif), theta=0, zeta=0, y=1+0.6*np.sin(angle_dif), z=2)
    wp.add_source(led1)
    wp.add_source(led2)
    wp.add_source(led3)
    wp.print_sources_list()

    wp.display_global_map()
    wp.display_global_map_contour()
    wp.display_working_space()