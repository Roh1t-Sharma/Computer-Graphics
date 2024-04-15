import matplotlib.pyplot as plt
import numpy as np
import random

# Define the number of points
NUMP = 20

# Define the point structure using a dictionary
points = [{'x': 0, 'y': 0, 'angle': 0} for _ in range(NUMP)]

# Generate random points
for point in points:
    point['x'] = random.randint(10, 390)
    point['y'] = random.randint(10, 390)

# Find the lowest point
lowest_point = min(points, key=lambda p: p['y'])

# Move the lowest point to the beginning of the list
points.remove(lowest_point)
points.insert(0, lowest_point)

# Function to calculate the polar angle
def polar_angle(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return np.arctan2(dy, dx) % (2 * np.pi)

# Calculate polar angles for each point relative to the lowest point
for point in points[1:]:
    point['angle'] = polar_angle(lowest_point['x'], lowest_point['y'], point['x'], point['y'])

# Sort points by polar angle
points = sorted(points[1:], key=lambda p: p['angle'])
points.insert(0, lowest_point)  # Re-insert the lowest point at the beginning

# Connect the points with lines to form a star polygon
x = [point['x'] for point in points]
y = [point['y'] for point in points]

# Ensure the star polygon is closed by adding the first point at the end
x.append(points[0]['x'])
y.append(points[0]['y'])

# Plot the points and the star polygon
plt.figure()
plt.scatter(x, y)
plt.plot(x, y, marker='o')

# Setting the aspect ratio to be equal to make the star look even
plt.axis('equal')

# Display the star polygon
plt.show()
