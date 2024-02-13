# Import necessary libraries
from math import sqrt
import networkx as nx
import sys

# Calculates time required to drive from one point to another in minutes
def euclidean_distance(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    result = sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return result

#
def total_cost(number_of_drivers, total_number_of_driven_minutes):
    result = 500 * number_of_drivers + total_number_of_driven_minutes
    return result

# Read in file info and return the points in a dictinary 
def read_file(file):
    points_dictionary = {}
    
    for line in file:
        line = line.strip()
        if line:
            load_number, pickup, dropoff = map(str.strip, line.split())
            points_dictionary[load_number] = {pickup, dropoff}
    
    return points_dictionary

# Calculate the total distance between each start and end point for each load ID
def distance_per_load(dictionary):
    load_distance = {}

    for load_id, points in dictionary.items():
        start_point = points['pickup']
        end_point = points['dropoff']
        distance = euclidean_distance(start_point, end_point)
        load_distance[load_id] = distance

    return load_distance

# Calculate the total distance between the start point of driver and start point for each load ID
def distance_per_start(dictionary):
    start_point = (0,0)
    start_to_load = {}

    for load_id, points in dictionary.items():
        pickup_point = points['pickup']
        distance = euclidean_distance(start_point, pickup_point)
        start_to_load[load_id] = distance

    return start_to_load

# 
def graph_creation(points_dictionary, load_distance, start_to_load):
    graph = nx.Graph()

    # Add nodes for each load
    for load_id, points in points_dictionary.items():
        graph.add_node(load_id, pos=points['pickup'])

    # Add edges with weights (distances)
    for load_id1, points1 in points_dictionary.items():
        for load_id2, points2 in points_dictionary.items():
            if load_id1 != load_id2:
                distance = load_distance[load_id1] + load_distance[load_id2]
                graph.add_edge(load_id1, load_id2, weight=distance)

    return graph

# 
def solve_vrp(file_path):
    points_dictionary = read_file(file_path)
    load_distance = distance_per_load(points_dictionary)
    start_to_load = distance_per_start(points_dictionary)

    G = graph_creation(points_dictionary, load_distance, start_to_load)
    
    drivers_schedule = []
    mst_edges = nx.minimum_spanning_edges(G, algorithm='kruskal', data=False)
    mst = nx.Graph()
    mst.add_edges_from(mst_edges)

    # Split the MST into separate components to represent different routes
    components = list(nx.connected_components(mst))

    for component in components:
        driver_schedule = list(component)
        drivers_schedule.append(driver_schedule)

    return drivers_schedule

# Create a main function
def main():
    if len(sys.argv) != 2:
        print("Error with number of arguments passed")
        sys.exit(1)

    file_path = sys.argv[1]
    drivers_schedule = solve_vrp(file_path)
    for schedule_per_driver in drivers_schedule:
        print(schedule_per_driver)