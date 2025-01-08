import pyvista as pv
import numpy as np
from pyvista import examples

# Constants
earth_radius = 6371 * 1000  # Earth's radius in meters
colors = {'PAYLOAD': 'blue', 'ROCKET BODY': 'yellow', 'DEBRIS': 'red'}  # Map object types to colors

def calculate_orbits(data, time_steps=100):
    """
    Calculate orbital paths based on apogee, perigee, and inclination.
    """
    orbits = []
    for _, row in data.iterrows():
        apogee = row['APOGEE'] * 1000  # Convert to meters
        perigee = row['PERIGEE'] * 1000  # Convert to meters
        inclination = np.radians(row['INCLINATION'])
        semi_major_axis = (apogee + perigee) / 2 + earth_radius
        eccentricity = (apogee - perigee) / (apogee + perigee + 2 * earth_radius)

        # Generate orbital points in 3D
        orbit_points = []
        for t in np.linspace(0, 2 * np.pi, time_steps):
            r = semi_major_axis * (1 - eccentricity**2) / (1 + eccentricity * np.cos(t))
            x = r * np.cos(t)
            y = r * np.sin(t) * np.cos(inclination)
            z = r * np.sin(t) * np.sin(inclination)  # Add z-coordinate
            orbit_points.append([x, y, z])
        orbits.append({'points': np.array(orbit_points), 'type': row['OBJECT_TYPE']})
    return orbits

def plot_earth_and_orbits(orbits):
    # Create a PyVista plotter with no default lighting
    pl = pv.Plotter(lighting="none")

    # Add a light source
    light = pv.Light()
    light.set_direction_angle(30, -20)
    light.intensity = 1.5
    pl.add_light(light)

    # Create a sphere to represent Earth with blue and green coloring
    earth_mesh = pv.Sphere(radius=earth_radius)
    earth_colors = earth_mesh.points[:, 2]  # Use z-coordinate for color gradient
    earth_mesh.point_data["colors"] = (earth_colors - np.min(earth_colors)) / (
        np.max(earth_colors) - np.min(earth_colors)
    )  # Normalize for gradient
    pl.add_mesh(
        earth_mesh,
        scalars="colors",
        cmap="Greens",
        clim=[0, 1],
        smooth_shading=True,
    )


    # Add a space-themed background using a cubemap
    cubemap = examples.download_cubemap_space_16k()
    pl.add_actor(cubemap.to_skybox())
    pl.set_environment_texture(cubemap, True)

    # Add orbital paths as lines
    for orbit in orbits:
        orbit_type = orbit['type']
        color = colors.get(orbit_type, 'gray')  # Default to gray if type is unknown
        points = orbit['points']
        for i in range(len(points) - 1):
            line = pv.Line(points[i], points[i + 1])
            pl.add_mesh(line, color=color, line_width=1)

    # Show the plot
    pl.show()
