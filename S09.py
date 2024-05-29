import pygame
import sys
import math

# Screen Dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Brightness of the light source and ambient light
amp = 0.9
ambient = 0.4
light = [-0.5, -0.5, -0.5]

# Vertices Coordinates
cube_vertices = [
    [-1.5, -1.5, -1.5],
    [1.5, -1.5, -1.5],
    [1.5, 1.5, -1.5],
    [-1.5, 1.5, -1.5],
    [-1.5, -1.5, 1.5],
    [1.5, -1.5, 1.5],
    [1.5, 1.5, 1.5],
    [-1.5, 1.5, 1.5]
]

# Cube faces
cube_faces = [
    [0, 1, 2, 3],  # Bottom face
    [7, 6, 5, 4],  # Top face
    [3, 7, 4, 0],  # Left face
    [1, 5, 6, 2],  # Right face
    [0, 4, 5, 1],  # Front face
    [2, 6, 7, 3]   # Back face
]

# Colors for the faces of the cube
face_colors = [
    (0, 100, 255),
    (100, 255, 0),
    (255, 100, 0),
    (0, 255, 255),
    (255, 0, 255),
    (255, 255, 0)
]

# Pygame Initialization
pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
fps_clock = pygame.time.Clock()

# Rotation angles
rotation_x = 0
rotation_y = 0


def rotate_along_x(point, angle):
    """ Rotating a point around the X-axis. """
    x, y, z = point
    rotated_y = y * math.cos(angle) - z * math.sin(angle)
    rotated_z = y * math.sin(angle) + z * math.cos(angle)
    return [x, rotated_y, rotated_z]


def rotate_along_y(point, angle):
    """ Rotating a point around the Y-axis. """
    x, y, z = point
    rotated_x = x * math.cos(angle) - z * math.sin(angle)
    rotated_z = x * math.sin(angle) + z * math.cos(angle)
    return [rotated_x, y, rotated_z]


def project_to_2d(point):
    """ Projecting a 3D point into 2D space. """
    fov = 256  # Field of view
    viewer_dist = 4  # Distance to the viewer
    x, y, z = point
    scale = fov / (z + viewer_dist)
    proj_x = x * scale + SCREEN_WIDTH / 2
    proj_y = y * scale + SCREEN_HEIGHT / 2
    return [int(proj_x), int(proj_y)]


def normalize(vector):
    """ Normalizing a vector. """
    length = math.sqrt(sum(coord ** 2 for coord in vector))
    return [coord / length for coord in vector]


def compute_vertex_intensity(vertex):
    """ Computing the light intensity at a vertex. """
    light_dir = normalize(light)
    normal = normalize(vertex)
    dot_product = sum(normal[i] * light_dir[i] for i in range(3))
    intensity = ambient + amp * max(0, dot_product)
    return min(1, intensity)


def interpolate_color(color, intensity):
    """ Interpolating the color considering the intensity. """
    r, g, b = color
    return (int(r * intensity), int(g * intensity), int(b * intensity))


def gouraud_shading(face, vertices, face_color):
    """ Shading a face using the Gouraud method. """
    intensities = [compute_vertex_intensity(vertices[vertex]) for vertex in face]
    avg_intensity = sum(intensities) / len(intensities)
    shaded_color = interpolate_color(face_color, avg_intensity)

    pygame.draw.polygon(window, shaded_color, [projected_2d_points[vertex] for vertex in face])


def is_visible(face, vertices):
    """ Checking the visibility of a face. """
    projected_points = [projected_2d_points[vertex] for vertex in face]
    x0, y0 = projected_points[0]
    x1, y1 = projected_points[1]
    x2, y2 = projected_points[2]
    x3, y3 = projected_points[3]

    S = (x0 - x1) * (y0 + y1) + (x1 - x2) * (y1 + y2) + (x2 - x3) * (y2 + y3) + (x3 - x0) * (y3 + y0)
    return S > 0


# Main loop
is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handling key presses for cube rotation
    key_input = pygame.key.get_pressed()
    rotation_x += (key_input[pygame.K_UP] - key_input[pygame.K_DOWN]) * 0.05
    rotation_y += (key_input[pygame.K_RIGHT] - key_input[pygame.K_LEFT]) * 0.05

    # Rotating and projecting the cube's points
    transformed_points = [rotate_along_y(rotate_along_x(p, rotation_x), rotation_y) for p in cube_vertices]
    projected_2d_points = [project_to_2d(p) for p in transformed_points]

    # Displaying the background
    window.fill(BLACK)

    # Drawing the cube's faces
    for i, face in enumerate(cube_faces):
        if is_visible(face, transformed_points):
            gouraud_shading(face, transformed_points, face_colors[i])

    # Updating the screen
    pygame.display.flip()
    # Limiting the frame rate
    fps_clock.tick(60)