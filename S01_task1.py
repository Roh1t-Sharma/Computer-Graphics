import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
import numpy as np

# Length of the side of the equilateral triangle
a = 2

# Calculate the height of the triangle
h = (a * np.sqrt(3)) / 2

# The coordinates of the vertices of the equilateral triangle (A, B, C)
A = (0, 0)
B = (a / 2, h)
C = (a, 0)

# Create a figure and an axis
fig, ax = plt.subplots()

# Draw the triangle
triangle = patches.Polygon([A, B, C], closed=True, fill=False, linestyle=':')
pc = PatchCollection([triangle], match_original=True)

# # Draw the circumcircle
# R = (a * np.sqrt(3)) / 3
# circumcircle = plt.Circle(B, R, fill=False, color='black', linestyle='-')

# Draw the inscribed circle
r = (a * np.sqrt(3)) / 6
inscribed_circle = plt.Circle((a / 2, r), r, color='blue', linestyle='-')

# Add the shapes to the plot
ax.add_collection(pc)
# ax.add_patch(circumcircle)
ax.add_patch(inscribed_circle)

# Set the aspect of the plot to be equal
ax.set_aspect('equal')

# Set limits to show the triangle in the center
plt.xlim(-1, 3)
plt.ylim(-1, 2)

# Remove axes for visual appeal
plt.axis('off')

# Show the plot
plt.show()
