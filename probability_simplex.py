import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.animation import FuncAnimation

# Set up the 3D plot
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Define the vertices of the simplex (the triangle in 3D space)
vertices = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
ax.plot_trisurf(vertices[:, 0], vertices[:, 1], vertices[:, 2], color='lightblue', alpha=0.6, edgecolor='gray')

# Generate points for a line traveling around the plane (inside the simplex)
t = np.linspace(0, 2 * np.pi, 100)
line_points = np.column_stack([0.5 + 0.5 * np.cos(t), 0.5 * np.sin(t), 1 - (0.5 + 0.5 * np.cos(t) + 0.5 * np.sin(t))])

# Plot the line on the simplex
ax.plot(line_points[:, 0], line_points[:, 1], line_points[:, 2], color='purple', lw=2, label='Line on Simplex')

# Add a point that moves along the line
point, = ax.plot([line_points[0, 0]], [line_points[0, 1]], [line_points[0, 2]], 'ro', label='Moving Point')

# Set axis limits and labels
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_zlim(0, 1)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.legend()


ax.view_init(elev=30, azim=45)
plt.show()
