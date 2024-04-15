from scipy.spatial import ConvexHull
import numpy as np
import matplotlib.pyplot as plt

# Generate random points
num_points = 100
points = np.random.rand(num_points, 2) * 100

# Compute the convex hull
hull = ConvexHull(points)

# Plot the points
plt.plot(points[:, 0], points[:, 1], 'o')

# Plot the convex hull
for simplex in hull.simplices:
    plt.plot(points[simplex, 0], points[simplex, 1], 'k-')

# Add the first point of the hull to close the shape
plt.plot(points[hull.vertices[0], 0], points[hull.vertices[0], 1], 'ro')

# Display the plot
plt.title('Convex Hull')
plt.show()
