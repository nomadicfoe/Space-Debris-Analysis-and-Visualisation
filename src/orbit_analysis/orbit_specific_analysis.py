import pandas as pd
import numpy as np
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# Earth radius in km
earth_radius = 6371

# Function to classify orbital class
def classify_orbit(perigee, apogee):
    if apogee <= 2000:  # LEO
        return 'LEO'
    elif 2000 < apogee <= 35786:  # MEO
        return 'MEO'
    else:  # GEO
        return 'GEO'

# Add orbital class to the dataset
def add_orbit_class(data):
    data['ORBIT_CLASS'] = data.apply(lambda x: classify_orbit(x['PERIGEE'], x['APOGEE']), axis=1)
    return data

# Orbit-Specific 3D Visualization
def visualize_orbit_class(data, title):
    phi = np.linspace(0, 2 * np.pi, 100)
    theta = np.linspace(0, np.pi, 100)
    x_sphere = earth_radius * np.outer(np.sin(theta), np.cos(phi))
    y_sphere = earth_radius * np.outer(np.sin(theta), np.sin(phi))
    z_sphere = earth_radius * np.outer(np.cos(theta), np.ones_like(phi))

    data['Radius'] = earth_radius + (data['APOGEE'] + data['PERIGEE']) / 2
    data['Inclination_rad'] = np.radians(data['INCLINATION'])
    data['Longitude_rad'] = np.random.uniform(0, 2 * np.pi, size=len(data))

    data['X'] = data['Radius'] * np.sin(data['Inclination_rad']) * np.cos(data['Longitude_rad'])
    data['Y'] = data['Radius'] * np.sin(data['Inclination_rad']) * np.sin(data['Longitude_rad'])
    data['Z'] = data['Radius'] * np.cos(data['Inclination_rad'])

    fig = go.Figure()
    fig.add_trace(go.Surface(x=x_sphere, y=y_sphere, z=z_sphere, colorscale='Blues', opacity=0.5))
    fig.add_trace(go.Scatter3d(x=data['X'], y=data['Y'], z=data['Z'],
                               mode='markers', marker=dict(size=3, color=data['INCLINATION'],
                               colorscale='Viridis', opacity=0.7, showscale=True)))
    fig.update_layout(title=title, scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))
    fig.show()

# Density Analysis for Debris Mitigation
def analyze_density(data):
    leo_objects = data[data['ORBIT_CLASS'] == 'LEO']
    sns.kdeplot(data=leo_objects, x='INCLINATION', y='APOGEE', cmap="Reds", fill=True, thresh=0.05, levels=100)
    plt.title('Density Analysis of LEO Objects (Debris Mitigation)')
    plt.xlabel('Inclination (degrees)')
    plt.ylabel('Apogee (km)')
    plt.grid()
    plt.show()

    # Identify high-density regions
    leo_high_density = leo_objects[(leo_objects['INCLINATION'] > 70) & (leo_objects['APOGEE'] < 2000)]
    print(f"High-Inclination LEO Objects: {len(leo_high_density)}")
    debris = leo_high_density[leo_high_density['OBJECT_TYPE'] == 'DEBRIS']
    print(f"High-Inclination LEO Debris: {len(debris)}")
    print(debris[['SATNAME', 'INCLINATION', 'APOGEE', 'PERIGEE']])
