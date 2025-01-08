import data_preprocessing as dp
import collision_detection as cd
import visualization as vz
from orbit_analysis import check_3, orbit_specific_analysis


def main():
    # File path to the dataset
    file_path = '/mnt/a71d6a0a-c8e5-4961-92b2-05e4d2a4cf53/Sumanth paila/Course work/Python/Final Project/Space Debris Visualisation  Project/data/space_track_final_data_3.csv'

    # Step 1: Load and preprocess the data
    print("Loading and preprocessing data...\n")
    data = dp.load_and_summarize_data(file_path, "Space-Track")
    preprocessed_data = dp.preprocess_data(
        data,
        cols_to_drop=['COMMENT', 'COMMENTCODE', 'RCS_SIZE'],
        cols_to_impute=['APOGEE', 'PERIGEE', 'INCLINATION']
    )

    # Main loop for user interaction
    while True:
        print("\nChoose Visualization:")
        print("1. Orbit Paths Visualization")
        print("2. Orbit Specific Analysis")
        print("3. Interactive Collision Detection")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            # Orbit Paths Visualization
            print("\nGenerating Orbit Paths Visualization...")
            orbits = check_3.calculate_orbits(preprocessed_data)
            check_3.plot_earth_and_orbits(orbits)

        elif choice == '2':
            # Orbit Specific Analysis
            print("\nGenerating Orbit Specific Analysis...")
            preprocessed_data = orbit_specific_analysis.add_orbit_class(preprocessed_data)
            print("Visualizing LEO, MEO, and GEO objects...")
            orbit_specific_analysis.visualize_orbit_class(preprocessed_data[preprocessed_data['ORBIT_CLASS'] == 'LEO'],
                                                          "LEO Objects")
            orbit_specific_analysis.visualize_orbit_class(preprocessed_data[preprocessed_data['ORBIT_CLASS'] == 'MEO'],
                                                          "MEO Objects")
            orbit_specific_analysis.visualize_orbit_class(preprocessed_data[preprocessed_data['ORBIT_CLASS'] == 'GEO'],
                                                          "GEO Objects")

            print("Analyzing density for debris mitigation in LEO...")
            orbit_specific_analysis.analyze_density(preprocessed_data)

        elif choice == '3':
            # Interactive Collision Detection
            print("\nRunning Interactive Collision Detection...")
            feature_columns = ['APOGEE', 'PERIGEE', 'INCLINATION']
            distances = cd.compute_pairwise_distances(preprocessed_data, feature_columns)
            collisions = cd.detect_collisions(distances, threshold=3.0)

            print("Visualizing collision risks in 3D...")
            vz.plot_interactive_3d_collisions(preprocessed_data, collisions, feature_columns, 'OBJECT_TYPE')
            vz.plot_interactive_collision_network(preprocessed_data, collisions, 'OBJECT_TYPE')

        elif choice == '4':
            # Exit the program
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
