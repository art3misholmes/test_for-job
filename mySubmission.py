# Import necessary libraries
from math import sqrt
import networkx as nx
import sys

# Calculates time required to drive from one point to another in minutes
def euclidean_distance(point_1, point_2):

    # Break the point into its x and y values (split tuple) 
    x1, y1 = point_1
    x2, y2 = point_2 

    # Use the euclidean distance formula
    result = sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # return the result from the euclidean distance formula
    return result

# Calculates total cost based on the number of drivers and total driven minutes
def total_cost(number_of_drivers, total_number_of_driven_minutes):

    # Use the total cost formula
    result = 500 * number_of_drivers + total_number_of_driven_minutes

    # Return the result of the total cost formula
    return result

# Read in file info and return the points in a dictionary 
def read_file(file):
    
    points_dictionary = {}
    
    for line in file:
        line = line.strip()
        if line:
            # Split the line into load number, pickup, and dropoff using whitespace as separator
            load_info = list(map(str.strip, line.split()))

            # Check if there are at least three values in load_info
            if len(load_info) >= 3:
                load_number, pickup, dropoff = load_info[:3]
                points_dictionary[load_number] = {'pickup': pickup, 'dropoff': dropoff}
            else:
                print(f"Skipping invalid line: {line}")

    return points_dictionary

# Calculate the total distance between each start and end point for each load ID
def distance_per_load(dictionary):

    # Initialize an empty dictionary to store the distance for each load
    load_distance = {}

    # Iterate through each load ID and its corresponding points in the dictionary
    for load_id, points in dictionary.items():

        # Extract the pickup point from the points dictionary
        start_point = points['pickup']

        # Extract the dropoff point from the points dictionary
        end_point = points['dropoff']

        # Calculate the Euclidean distance between the pickup and dropoff points
        distance = euclidean_distance(start_point, end_point)

        # Store the calculated distance in the load_distance dictionary
        load_distance[load_id] = distance

    # Return the dictionary containing the distances for each load
    return load_distance

# Calculate the total distance between the start point of the driver and the start point for each load ID
def distance_per_start(dictionary):

    # Define the starting point as the origin (0, 0)
    start_point = (0,0)

    # Initialize an empty dictionary to store the distance from the starting point to each load
    start_to_load = {}

    # Iterate through each load ID and its corresponding points in the dictionary
    for load_id, points in dictionary.items():

        # Extract the pickup point from the points dictionary
        pickup_point = points['pickup']

        # Calculate the Euclidean distance from the starting point to the pickup point
        distance = euclidean_distance(start_point, pickup_point)

        # Store the calculated distance in the start_to_load dictionary
        start_to_load[load_id] = distance

    # Return the dictionary containing the distances from the starting point to each load
    return start_to_load

# Create a graph based on points, load distances, and distances from start to each load
def graph_creation(points_dictionary, load_distance, start_to_load):

    # Create an undirected graph using NetworkX
    graph = nx.Graph()

    # Add nodes for each load in the points_dictionary
    for load_id, points in points_dictionary.items():

        # Add a node with the load_id as the label and the pickup point as the 'pos' attribute
        graph.add_node(load_id, pos=points['pickup'])

    # Add edges with weights (distances) between all pairs of loads in points_dictionary
    for load_id1, points1 in points_dictionary.items():

        # Iterate through all other loads in points_dictionary
        for load_id2, points2 in points_dictionary.items():

            # Ensure not adding self-loops
            if load_id1 != load_id2:

                # Calculate the total distance as the sum of distances for both loads
                distance = load_distance[load_id1] + load_distance[load_id2]

                # Add an edge between load_id1 and load_id2 with weight equal to the calculated distance
                graph.add_edge(load_id1, load_id2, weight=distance)

    # Return the created graph
    return graph

# Solve the Vehicle Routing Problem (VRP) using the given file path
def VRP(file_path):

    # Read file and create a points dictionary
    points_dictionary = read_file(file_path)

    # Calculate distances per load
    load_distance = distance_per_load(points_dictionary)

    # Calculate distances from the starting point to each load
    start_to_load = distance_per_start(points_dictionary)

    # Create a graph using points, load distances, and distances from start to each load
    graph = graph_creation(points_dictionary, load_distance, start_to_load)

    # Initialize an empty list to store the schedule for each driver
    drivers_schedule = []

    # Find the Minimum Spanning Tree (MST) using Kruskal's algorithm
    mst_edges = nx.minimum_spanning_edges(graph, algorithm='kruskal', data=False)

    # Create a new graph for the MST
    mst = nx.Graph()

    # Add edges to the MST graph
    mst.add_edges_from(mst_edges)

    # Split the MST into separate components to represent different routes
    components = list(nx.connected_components(mst))

    # Iterate through each component in the MST
    for component in components:

        # Convert the component to a list and add it to the drivers_schedule list
        driver_schedule = list(component)

    # Append the current driver_schedule list to the overall drivers_schedule list
    drivers_schedule.append(driver_schedule)

    # Return the list of driver schedules
    return drivers_schedule

# Main function to be executed when the script is run
def main():
    # Check if the number of command-line arguments is not equal to 2
    if len(sys.argv) != 2:

        # Print an error message
        print("Error with the number of arguments passed")

        # Exit the script with a status code of 1
        sys.exit(1)

    # Retrieve the file path from the command-line arguments
    file_path = sys.argv[1]

    try:

        # Open the file in read mode
        with open(file_path, 'r') as file:

            # Solve the Vehicle Routing Problem (VRP) using the provided file path
            drivers_schedule = VRP(file)

            # Iterate through each schedule_per_driver in the list of driver schedules
            for schedule_per_driver in drivers_schedule:

                # Print the schedule for each driver
                print(schedule_per_driver)

    except FileNotFoundError:

        # Print an error message if the file is not found
        print(f"Error: File '{file_path}' not found.")

main()