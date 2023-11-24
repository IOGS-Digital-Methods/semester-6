import numpy as np
import matplotlib.pyplot as plt


def calculate_irradiance(position, normal, sources):
    """
    Calculate irradiance at a given position on the surface.

    Parameters:
        position (np.array): 3D coordinates of the point on the surface.
        normal (np.array): Normal vector at the given position on the surface.
        sources (list): List of light sources, where each source is a tuple (source_position, intensity, incident_angle, inclination_angle).

    Returns:
        irradiance (float): Total irradiance at the given position.
    """
    irradiance = 0.0
    for source_position, intensity, incident_angle, inclination_angle in sources:
        light_direction = source_position - position
        light_direction = light_direction / np.linalg.norm(light_direction)

        cos_theta = np.dot(light_direction, normal)
        sin_phi = np.sin(np.radians(inclination_angle))

        distance = np.linalg.norm(position - source_position)
        irradiance += intensity * cos_theta * sin_phi / (4 * np.pi * distance ** 2)
    return irradiance


def generate_irradiance_map(surface_size, sources):
    """
    Generate an irradiance map for a surface with punctual light sources.

    Parameters:
        surface_size (tuple): Size of the surface (width, height).
        sources (list): List of light sources, where each source is a tuple (source_position, intensity, incident_angle, inclination_angle).

    Returns:
        irradiance_map (np.array): 2D array representing the irradiance map.
    """
    width, height = surface_size
    irradiance_map = np.zeros((width, height))

    for i in range(width):
        for j in range(height):
            position = np.array([i, j, 0])  # Assuming a 2D surface in the xy-plane
            normal = np.array([0, 0, 1])  # Assuming the normal vector is pointing in the positive z-direction
            irradiance_map[i, j] = calculate_irradiance(position, normal, sources)

    return irradiance_map


# Example usage:
light_sources = [
    (np.array([50, 50, 100]), 100, 45, 90),
    # Example light source at position [5, 5, 10] with intensity 100, incident angle 45 degrees, and inclination angle 30 degrees
]

surface_size = (200, 200)  # Adjust the size of the surface as needed
irradiance_map = generate_irradiance_map(surface_size, light_sources)

# Display the irradiance map using matplotlib
plt.imshow(irradiance_map, cmap='viridis', origin='lower', extent=(0, surface_size[0], 0, surface_size[1]))
plt.colorbar(label='Irradiance')
plt.title('Irradiance Map')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()