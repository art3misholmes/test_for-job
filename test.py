# Import necessary libraries
from math import sqrt

# Define functions for given equations

# Calculates time required to drive from one point to another in minutes
def euclidean_distance(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    result = sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return result

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

# 