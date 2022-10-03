# Author: A.Wachholz
# Date: 03.10.22

# imports
import sys
import numpy as np
import pandas as pd

sys.path.append('tools/')
from macronutrient_ternary_subplot import *


# define constants
SQRT3 = np.sqrt(3)                            
SQRT3OVER2 = SQRT3 / 2                       


# define functions


def distance_between_points(p1, p2):
    
    """
    :param p1: 2 tuple with (x, y)
    :param p2: 2 tuple with (x, y)
    :returns: distance between p1 and p2
    """

    return np.sqrt(
        (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2
        )


def project_point(p):
    """
    Maps (x,y,z) coordinates to ternary plot coordinates.
    Parameters
    ----------
    p: 3-tuple
        The point to be projected p = (x, y, z)
        The order of the coordinates, counterclockwise from the origin
    """
    a = p[0]
    b = p[1]
    x = a + b / 2.
    y = SQRT3OVER2 * b
    return np.array([x, y])



def dist_metric(points):
    
    """
    :param point: list of 3 tuples containing coordinates in ternary space
    :returns: sum of distances between points -> sort input by month!

    """

    # * convert coordinates to cartesian
    points_cartesian = [project_point(x) for x in points]
    # * calculate and sum up distances
    n_points = len(points_cartesian)
    dist = 0
    for i in range(n_points):
        dist += distance_between_points(
                points_cartesian[(i) % n_points],
                points_cartesian[(i + 1) % n_points] 
            )

    return dist



if __name__ == "__main__":

    # define test cases
    test_cases_in = [
        [(100, 0, 0), (0, 100, 0)],
        [(100, 0, 0), (0, 100, 0), (0, 0, 100)],
        [(100/3, 100/3, 100/3), (100/3, 100/3, 100/3)]
    ]
    test_cases_out = [200, 300, 0]

    # run tests
    for i in range(3):
        if dist_metric(test_cases_in[i]) == test_cases_out[i]:
            pass
        else:
            raise(ValueError, 'test failed')    











