import matplotlib.pyplot as plt
import numpy as np
import random


# Function to know if we have a counter-clockwise turn
def ccw(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])


# Graham scan algorithm to find the convex hull
def graham_scan(points):
    # Find the point with the lowest y-coordinate, break ties by x-coordinate
    start = min(points, key=lambda p: (p[1], p[0]))
    points.pop(points.index(start))

    # Sort the points by polar angle with the start point
    points.sort(key=lambda p: (np.arctan2(p[1] - start[1], p[0] - start[0]),
                               -p[1]))

    # Initialize the convex hull with the start point
    hull = [start]

    for point in points:
        while len(hull) > 1 and ccw(hull[-2], hull[-1], point) <= 0:
            hull.pop()
        hull.append(point)

    # Close the hull by adding the start point at the end
    hull.append(start)

    return hull


# Generate a set of random points
num_points = 15
points = [(random.uniform(-100, 100), random.uniform(-100, 100)) for _ in range(num_points)]

# Perform Graham Scan to find the convex hull
hull_points = graham_scan(points)

# Unpack the points for plotting
x, y = zip(*points)
hx, hy = zip(*hull_points)

# Plot the set of points
plt.scatter(x, y, label='Points')

# Plot the convex hull
plt.plot(hx, hy, 'r-', label='Convex Hull')

# Show the plot with a legend
plt.legend()
plt.title('Convex Hull with Graham scan algorithm')
plt.show()
