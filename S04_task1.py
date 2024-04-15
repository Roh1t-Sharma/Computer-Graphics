import matplotlib.pyplot as plt
import numpy as np

# Define the x range for which we will plot the sine function
x = np.linspace(-2 * np.pi, 2 * np.pi, 1000)

# Parameters for shifting and scaling
shift_x = 1
shift_y = 2
scale_x = 3
scale_y = 4

# Apply shifting and scaling to the sine function
y = scale_y * np.sin(scale_x * (x - shift_x)) + shift_y

plt.plot(x, np.sin(x), label='Original y=sin(x)')

plt.plot(x, y, label='Scaled and Shifted y=sin(x)')

# Adding title and labels
plt.title('Shifted and Scaled Sine Function')
plt.xlabel('x')
plt.ylabel('y')

plt.legend()
plt.show()
