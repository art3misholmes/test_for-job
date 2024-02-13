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

# Read in file info from command line argument