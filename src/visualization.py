import plotly.graph_objects as go
import networkx as nx
from scipy.spatial.distance import cdist
import pandas as pd
import numpy as np


def compute_pairwise_distances(data, feature_columns):
    """
    Compute pairwise distances between all objects based on the given features.
    """
    positions = data[feature_columns].values  # Extract the features for distance calculation
    distances = cdist(positions, positions)  # Pairwise Euclidean distance
    return distances


def detect_collisions(distances, threshold=1.0):
    """
    Identify pairs of objects with distances below the collision threshold.
    """
    collision_pairs = np.where((distances < threshold) & (distances > 0))

    # Create a DataFrame to represent collisions
    collisions = pd.DataFrame({
        'Object_1': collision_pairs[0],
        'Object_2': collision_pairs[1],
        'Distance': distances[collision_pairs]
    })

    # Drop duplicate pairs (e.g., (A, B) and (B, A))
    collisions = collisions[collisions['Object_1'] < collisions['Object_2']]

    return collisions


def plot_interactive_3d_collisions(data, collisions, feature_columns, object_type_column):
    """
    Interactive 3D scatter plot using Plotly, showing objects and potential collision pairs.
    """
    x_col, y_col, z_col = feature_columns
    object_types = data[object_type_column].unique()

    # Assign a unique color to each object type
    color_map = {obj_type: color for obj_type, color in zip(object_types, ['red', 'blue', 'pink'])}

    # Reset the index of the data to ensure integer-based indexing
    data = data.reset_index(drop=True)

    # Create the 3D scatter plot
    fig = go.Figure()

    # Add each object type to the plot
    for obj_type in object_types:
        subset = data[data[object_type_column] == obj_type]
        fig.add_trace(go.Scatter3d(
            x=subset[x_col], y=subset[y_col], z=subset[z_col],
            mode='markers',
            marker=dict(size=5, color=color_map[obj_type]),
            name=obj_type
        ))

    # Add lines for collision pairs
    for _, row in collisions.iterrows():
        try:
            i, j = int(row['Object_1']), int(row['Object_2'])  # Ensure indices are integers
            fig.add_trace(go.Scatter3d(
                x=[data.loc[i, x_col], data.loc[j, x_col]],
                y=[data.loc[i, y_col], data.loc[j, y_col]],
                z=[data.loc[i, z_col], data.loc[j, z_col]],
                mode='lines',
                line=dict(color='red', width=2),
                name='Collision Risk'
            ))
        except KeyError:
            print(f"Warning: Collision indices {i} or {j} are out of bounds.")
            continue

    # Update layout
    fig.update_layout(
        title="Interactive 3D Visualization of Potential Collisions",
        scene=dict(
            xaxis_title=f"{x_col} (units)",
            yaxis_title=f"{y_col} (units)",
            zaxis_title=f"{z_col} (units)"
        ),
        legend=dict(itemsizing='constant')
    )

    fig.show()





def plot_interactive_collision_network(data, collisions, object_type_column):
    """
    Interactive network graph using Plotly, showing nodes and edges color-coded by object type.
    """
    G = nx.Graph()

    # Add nodes with attributes
    for idx, row in data.iterrows():
        G.add_node(idx, object_type=row[object_type_column])

    # Add edges for collision pairs
    for _, row in collisions.iterrows():
        G.add_edge(row['Object_1'], row['Object_2'], weight=row['Distance'])

    # Create node positions
    pos = nx.spring_layout(G)

    # Create Plotly traces for edges
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color='red'),
        hoverinfo='none',
        mode='lines'
    )

    # Create Plotly traces for nodes
    node_x = []
    node_y = []
    node_color = []
    node_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_info = f"Object Type: {G.nodes[node]['object_type']}<br>Node ID: {node}"
        node_text.append(node_info)
        node_color.append(hash(G.nodes[node]['object_type']) % 100)  # Assign a unique color

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        text=node_text,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            size=10,
            color=node_color,
            colorscale='Viridis',
            line_width=2
        )
    )

    # Create the Plotly figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Interactive Collision Network',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)
                    ))

    fig.show()
