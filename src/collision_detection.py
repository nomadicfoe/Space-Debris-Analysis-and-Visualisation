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
