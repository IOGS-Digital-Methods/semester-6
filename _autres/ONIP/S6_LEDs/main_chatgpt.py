import numpy as np
import matplotlib.pyplot as plt


def calculate_irradiance(position, sources):
    """
    Calculate irradiance at a given position on the surface.

    Parameters:
        position (np.array): 3D coordinates of the point on the surface.
        sources (list): List of light sources, where each source is a tuple (source_position, intensity).

    Returns:
        irradiance (float): Total irradiance at the given position.
    """
    irradiance = 0.0
    for source_position, intensity in sources:
        distance = np.linalg.norm(position - source_position)
        irradiance += intensity / (4 * np.pi * distance ** 2)
    return irradiance


def generate_irradiance_map(surface_size, sources):
    """
    Generate an irradiance map for a surface with punctual light sources.

    Parameters:
        surface_size (tuple): Size of the surface (width, height).
        sources (list): List of light sources, where each source is a tuple (source_position, intensity).

    Returns:
        irradiance_map (np.array): 2D array representing the irradiance map.
    """
    width, height = surface_size
    irradiance_map = np.zeros((width, height))

    for i in range(width):
        for j in range(height):
            position = np.array([i, j, 0])  # Assuming a 2D surface in the xy-plane
            irradiance_map[i, j] = calculate_irradiance(position, sources)

    return irradiance_map


# Example usage:
light_sources = [
    (np.array([50, 50, 10]), 100),  # Example light source at position [5, 5, 10] with intensity 100
    (np.array([10, 10, 10]), 50),  # Another light source at position [10, 10, 10] with intensity 50
]

surface_size = (100, 100)  # Adjust the size of the surface as needed
irradiance_map = generate_irradiance_map(surface_size, light_sources)

# Display the irradiance map using matplotlib
plt.imshow(irradiance_map, cmap='viridis', origin='lower', extent=(0, surface_size[0], 0, surface_size[1]))
plt.colorbar(label='Irradiance')
plt.title('Irradiance Map')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()