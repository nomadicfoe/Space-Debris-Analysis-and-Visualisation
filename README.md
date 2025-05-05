# Space Debris Visualization and Analysis

This project provides tools for analyzing and visualizing orbital paths, debris density, and collision risks in space. The project uses Python libraries such as PyVista, Plotly, Pandas, and Matplotlib to handle data preprocessing, visualization, and collision detection.

## Project Structure
The project is organized into multiple Python modules for modularity and reusability:

```
project/
|-- data/                              # Folder containing dataset files
|    |-- space_track_final_data.csv_1.py                          # Complete dataset (full data)
|    |-- space_track_final_data.csv_2.py                          # Sample dataset (subset of full data)
|    |-- space_track_final_data.csv_3.py                          # Small dataset (for testing)
|
|-- main.py                            # Main script to run the project
|-- data_preprocessing.py              # Module for data loading and preprocessing
|-- collision_detection.py             # Module for collision detection
|-- visualization.py                   # Module for interactive 3D visualizations
|-- orbit_analysis/                    # Package for orbit-specific analysis
|    |-- __init__.py                   # Init file for the package
|    |-- check_3.py                    # Visualization of orbital paths around Earth
|    |-- orbit_specific_analysis.py    # Analysis of LEO, MEO, GEO orbits and debris
```

## Prerequisites
To run this project, you need the following libraries installed:
- Python 3.8+
- Pandas
- NumPy
- PyVista
- Plotly
- Matplotlib
- Seaborn
- Scipy
- NetworkX

You can install the required packages using the following command:
```bash
pip install pandas numpy pyvista plotly matplotlib seaborn scipy networkx
```

## How to Run the Project
1. Clone the repository and navigate to the project directory.
2. Ensure that the `data` folder contains the dataset files (1.py, 2.py, 3.py).
3. Run the main script:
   ```bash
   python main.py
   ```

4. Follow the interactive menu to select visualizations:
   - **Option 1**: Orbit Paths Visualization
   - **Option 2**: Orbit Specific Analysis
   - **Option 3**: Interactive Collision Detection
   - **Option 4**: Exit

## Features
### 1. Orbit Paths Visualization
- Visualizes orbital paths around Earth in 3D.
- Displays a smooth Earth sphere with a space-themed background.
- Uses PyVista for rendering.

### 2. Orbit Specific Analysis
- Classifies objects into three orbital classes: **LEO (Low Earth Orbit)**, **MEO (Medium Earth Orbit)**, and **GEO (Geostationary Orbit)**.
- Visualizes objects in each orbital class using 3D scatter plots (Plotly).
- Analyzes debris density in LEO using Seaborn's KDE plots.
- Identifies high-density regions for debris mitigation strategies.

### 3. Interactive Collision Detection
- Computes pairwise distances between space objects to detect collision risks.
- Provides two interactive visualizations:
   - **3D Scatter Plot**: Displays space objects and highlights collision pairs.
   - **Network Graph**: Displays collision risks as a network of nodes and edges.

## Data Folder
The `data` folder includes three versions of the dataset for testing and scaling purposes:
1. **space_track_final_data.csv_1.py**: Complete dataset containing all objects.
2. **space_track_final_data.csv_2.py**: A smaller sample of the dataset.
3. **space_track_final_data.csv_3.py**: A small subset of the dataset for quick testing.

## Example Workflow
1. **Load Data**: The data is loaded and summarized using `data_preprocessing.py`.
2. **Preprocessing**: Missing values are imputed, unnecessary columns are dropped, and data integrity is checked.
3. **Orbit Paths**: `check_3.py` generates 3D orbit visualizations around Earth.
4. **Orbit Analysis**: `orbit_specific_analysis.py` performs orbit classification and density analysis.
5. **Collision Detection**: `collision_detection.py` detects and visualizes collision risks interactively.

## Sample Results
1. **Orbit Paths**:  3D orbit visualizations around Earth
   ![WhatsApp Image 2024-12-07 at 23 59 56](https://github.com/user-attachments/assets/faff3ccd-4364-4212-b72d-a01b42b14880)
2. **Orbit Analysis**: orbit classification and density analysis.
   ![WhatsApp Image 2024-12-08 at 00 07 04](https://github.com/user-attachments/assets/5166c6a6-42d3-48fe-af50-e4841a7b237b)
   ![WhatsApp Image 2024-12-08 at 00 06 21](https://github.com/user-attachments/assets/4bb4af54-ec1e-4e9a-a2c4-42c37c39b1a5)
   ![WhatsApp Image 2024-12-08 at 00 05 02](https://github.com/user-attachments/assets/7e441330-7ebd-4e77-800f-b89bfe75427c)

4. **Collision Detection**: detects and visualizes collision risks interactively.
   ![WhatsApp Image 2024-12-08 at 00 05 22](https://github.com/user-attachments/assets/4d04f659-7c11-4835-9d1d-200ab999d844)
   ![WhatsApp Image 2024-12-08 at 00 03 52](https://github.com/user-attachments/assets/5101d635-a922-416a-930d-d2d8916b1e28)
   ![WhatsApp Image 2024-12-08 at 00 03 13](https://github.com/user-attachments/assets/bca8a33a-f4ba-41a1-9cf5-bb93787233dc)

### Author
Developed by **Sumanth Paila**
