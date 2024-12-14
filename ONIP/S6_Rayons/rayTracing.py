'''
Exemple de code de tracé de rayons ONIP S6 2024
Cas d'un point objet à l'infini sur l'axe uniquement
Chromatisme
Champ ajustable
Autofocus sur la taille de tache RMS

'''

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

class Material:
    #Bs and Cs are Seidel coeffs
    def __init__(self, Bs, Cs):
        self.Bs = np.array(Bs)
        self.Cs = np.array(Cs)

    def get_optical_index(self, wavelength):
        return np.sqrt(1+np.sum(self.Bs*wavelength**2/(wavelength**2 - self.Cs)))


class Materials_Library:
    BK7 = Material([1.03961212, 0.231792344, 1.01046945], [0.00600069867, 0.0200179144, 103.560653])
    NSF2 = Material([1.47343127, 0.163681849, 1.36920899], [0.0109019098, 0.0585683687, 127.404933])
    VACCUUM = Material([0, 0, 0], [0, 0, 0])


class Ray:
    def __init__(self, delta, p0, wavelength):
        self.delta = delta
        self.p0 = p0
        self.wavelength = wavelength

    def __str__(self):
        return "delta " + str(self.delta) + "  p0 "+str(self.p0)

    def get_point(self, t):
        return self.delta*t+self.p0

    def get_intersection_zplane(self, z):
        return self.get_point((z-self.p0[2])/self.delta[2])

    def get_xy_position(self):
        return self.p0[0:2]


class Surface:
    def __init__(self, radius, thickness, material, is_mirror = False):
        self.radius = radius
        self.thickness = thickness
        self.material = material
        self.is_mirror = is_mirror
        self.center = np.zeros(3)

    def set_z(self, z):
        self.z = z
        self.center = np.array([0, 0, z+self.radius])

    def propagate(self, ray, material_before, dz = 0):
        if self.radius == 0:
            p_i = ray.get_intersection_zplane(self.z + dz)
            normal = np.array([0, 0, 1])
        else:
            if dz != 0:
                raise("Non zero defocus for spherical surf", "Defocus is only taken into account for plane surfaces")
            alpha = np.sum(ray.delta**2)
            beta = 2*np.sum(ray.delta * (ray.p0 - self.center))
            gamma = np.sum((ray.p0 - self.center)**2)-self.radius**2
            delta = beta**2 - 4 * alpha * gamma
            t_plus = (-beta - np.sqrt(delta))/2/alpha
            t_minus = (-beta + np.sqrt(delta))/2/alpha
            t = t_plus if np.abs(
                t_plus-self.z) < np.abs(t_minus-self.z) else t_minus
            p_i = ray.get_point(t)
            normal = p_i - self.center
            normal /= np.linalg.norm(normal)
        theta = np.arccos(np.dot(normal, ray.delta))
        if (theta == 0 or np.cos(theta) == 1):
            return Ray(ray.delta, p_i, ray.wavelength)
        else:
            tang = ray.delta - normal * np.cos(theta)
            if (np.linalg.norm(tang) == 0):
                return Ray(ray.delta, p_i, ray.wavelength)
            tang /= np.linalg.norm(tang)
            if (self.is_mirror):
                theta_p = -theta
            else:
                theta_p = np.arcsin(material_before.get_optical_index(
                    ray.wavelength)/self.material.get_optical_index(ray.wavelength)*np.sin(theta))
                if (theta > np.pi/2):
                    theta_p = np.pi-theta_p
            return Ray(np.cos(theta_p)*normal + np.sin(theta_p)*tang, p_i, ray.wavelength)

class Spotdiag_data:
    def __init__(self, fields, wavelength):
        self.fields = fields
        self.wavelength = wavelength
        self.data = [[0 for i in range(len(wavelength))] for j in range(len(fields))]

    def add_data(self, field_index, wavelength_index, data):
        if field_index>=len(self.fields) or field_index<0:
            raise("Exception", "Wrong Field index")
        if wavelength_index>=len(self.wavelength) or wavelength_index<0:
            raise("Exception", "Wrong Wavelength index")
        self.data[field_index][wavelength_index] = data

    
    def __get_rms_radius(self, xy_positions):
        mean = np.mean(xy_positions, 0)
        return np.sqrt(np.sum([[np.linalg.norm(xy_positions-mean)**2 for i in range(0, len(xy_positions))]]))/len(xy_positions)
    
    def get_rms_radius00(self):
        return self.__get_rms_radius(self.data[0][0])
    
    def plot_all(self):
        axes = plt.subplots(1,len(self.fields))
        for f in range(0, len(self.fields)):
            if (len(self.fields) == 1):
                ax = axes[1]
            else:
                ax = axes[1][f]
            str_rms = ""
            for w in range(0, len(self.wavelength)):
                ax.scatter(self.data[f][w][:, 0], self.data[f][w][:, 1], label=str(self.wavelength[w]), s=5)
                str_rms += str(np.round(self.__get_rms_radius(self.data[f][w])*1000,1))+" µm / "
            str_rms = str_rms[:-2]
            ax.text(0.5,0.02, str_rms, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
            ax.legend(loc='upper right', shadow=True, fontsize='x-large')
        plt.show()

class Optical_system:
    def __init__(self, entrance_pupil_diam):
        self.entrance_pupil_diam = entrance_pupil_diam
        self.surfaces = []
        self.defocus = 0

    def add_a_surface(self, surface):
        self.surfaces.append(surface)
        self.prepare()

    def add_img_surface(self):
        self.add_a_surface(Surface(0, 0, Materials_Library.VACCUUM))

    def prepare(self):
        total_thickness = 0
        for i in range(0, len(self.surfaces)):
            self.surfaces[i].set_z(total_thickness)
            total_thickness += self.surfaces[i].thickness

    def minimize_rms_spot_size(self, field, wavelength):
        def min_search(dz): return self.__calculate_rms_radius(field, wavelength, dz)
        res = minimize(min_search, 0)
        self.defocus = res.x[0]
        print("Autofocus, dz = "+str(self.defocus))

    def __calculate_rms_radius(self, field, wavelength, defocus):
        nb_rays = 50
        nb_rings = 10
        self.defocus = defocus      
        return self.propagate_through([field], [wavelength], nb_rays, False, nb_rings).get_rms_radius00()

    def __get_rays_polar(self, field, wavelength, nb_rays, nb_rings):
        if (nb_rays%nb_rings != 0):
            nb_rays = nb_rings * int(np.ceil(nb_rays/nb_rings))
        nb_angles = np.floor_divide(nb_rays,nb_rings)
        r_vals = np.sqrt(np.linspace(0, 1, nb_rings))*self.entrance_pupil_diam/2
        dtheta = 2*np.pi/nb_angles
        rays = []
        for i in range(0, nb_rays):
            ring_ind = np.floor_divide(i,nb_angles)
            ang_ind = np.mod(i, nb_angles)
            r = r_vals[ring_ind]
            theta = dtheta * ang_ind
            p0 = np.array([r*np.cos(theta), r*np.sin(theta), 0])
            rays.append(Ray(np.array([0., np.sin(field/180*np.pi), np.cos(field/180*np.pi)]), p0, wavelength))
        return rays

    def __get_rays_rand(self, field, wavelength, nb_rays):
        def get_rand_p0_disk():
            module = self.entrance_pupil_diam/2*np.sqrt(np.random.random()) 
            angle = np.random.random()*2*np.pi
            return np.array([module*np.cos(angle), module*np.sin(angle), 0])
        rays = []
        for i in range(0, nb_rays):
            p0 = get_rand_p0_disk()
            rays.append(Ray(np.array([0., np.sin(field/180*np.pi), np.cos(field/180*np.pi)]), p0, wavelength))
        return rays

    def __get_rays(self, field, wavelength, nb_rays, rand_pos, nb_rings):
        if (rand_pos):
            return self.__get_rays_rand(field, wavelength, nb_rays)
        else:
            return self.__get_rays_polar(field, wavelength, nb_rays, nb_rings)

    def propagate_through(self, field_tab=[0], wavelength_tab=[0.55], nb_rays = 30, rand_pos = True, nb_rings = 6):
        spot_diag_data = Spotdiag_data(field_tab, wavelength_tab)
        prev_material = Materials_Library.VACCUUM
        for w in range(0, len(wavelength_tab)):
            for f in range(0, len(field_tab)):
                wavelength = wavelength_tab[w]
                field = field_tab[f]
                rays = self.__get_rays(field, wavelength, nb_rays, rand_pos, nb_rings)
                for i in range(0, len(self.surfaces)):
                    for j in range(0, len(rays)):
                        rays[j] = self.surfaces[i].propagate(rays[j], prev_material, self.defocus if i == len(self.surfaces)-1 else 0)
                    prev_material = self.surfaces[i].material
                spot_diag_data.add_data(f, w, np.array([rays[i].get_xy_position() for i in range(0, len(rays))]))        
        return spot_diag_data


plt.close('all')

nb_rays = 3000

wavelength_tab = [0.486, 0.588, 0.656]

'''
Lentille de focale 203 mm 
Champs : 0; 2 et 5°
Lambda = 486 nm; 588 nm et 656 nm
Autofocus
'''
singlet = Optical_system(25)
singlet.add_a_surface(Surface(105, 2, Materials_Library.BK7))
singlet.add_a_surface(Surface(0, 191.588, Materials_Library.VACCUUM))
singlet.add_img_surface()

singlet.minimize_rms_spot_size(0, wavelength_tab[1])

spot_diag_data = singlet.propagate_through([0, 2, 5], wavelength_tab, nb_rays)
spot_diag_data.plot_all()

'''
Doublet de 200 mm
Champs : 0; 2 et 5°
Lambda = 486 nm; 588 nm et 656 nm
Autofocus
'''
doublet = Optical_system(25)
doublet.add_a_surface(Surface(106.2, 10.6, Materials_Library.BK7))
doublet.add_a_surface(Surface(-92.2, 6.0, Materials_Library.NSF2))
doublet.add_a_surface(Surface(-409.4, 185, Materials_Library.VACCUUM))
doublet.add_img_surface()

doublet.minimize_rms_spot_size(0, wavelength_tab[1])

spot_diag_data = doublet.propagate_through([0, 2, 5], wavelength_tab, nb_rays)
spot_diag_data.plot_all()

'''
Miroir de rayon de courbure -300 mm 
Champs : 0; 2 et 5°
Lambda = 588 nm
Pas d'autofocus
'''
mirror = Optical_system(25)
mirror.add_a_surface(Surface(-300, -150, Materials_Library.VACCUUM, True))
mirror.add_img_surface()

spot_diag_data = mirror.propagate_through([0, 2, 5], [wavelength_tab[1]], nb_rays)
spot_diag_data.plot_all()
