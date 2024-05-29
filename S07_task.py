# import pygame
# import sys
# import numpy as np
#
# # Initialize Pygame
# pygame.init()
#
# # Constants
# WIDTH, HEIGHT = 1200, 700
#
# # Set up the display
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Cube")
#
# clock = pygame.time.Clock()
#
# cube_points = np.array([
#     [-1.5, -1.5, -1.5],
#     [1.5, -1.5, -1.5],
#     [1.5, 1.5, -1.5],
#     [-1.5, 1.5, -1.5],
#     [-1.5, -1.5, 1.5],
#     [1.5, -1.5, 1.5],
#     [1.5, 1.5, 1.5],
#     [-1.5, 1.5, 1.5]
# ])
#
# faces = [
#     [0, 4, 5, 1],  # Front face
#     [0, 1, 2, 3],  # Back face
#     [0, 3, 7, 4],  # Top face
#     [5, 4, 7, 6],  # Bottom face
#     [1, 5, 6, 2],  # Right face
#     [2, 6, 7, 3]  # Left face
# ]
#
#
# def rotateY(points, _angle):
#     """ Rotate the point around the Y axis by the given angle """
#     rotation_matrix = np.array([
#         [np.cos(_angle), 0, np.sin(_angle)],
#         [0, 1, 0],
#         [-np.sin(_angle), 0, np.cos(_angle)]
#     ])
#     return np.dot(points, rotation_matrix)
#
#
# def rotateX(points, _angle):
#     """ Rotate the point around the X axis by the given angle """
#     rotation_matrix = np.array([
#         [1, 0, 0],
#         [0, np.cos(_angle), -np.sin(_angle)],
#         [0, np.sin(_angle), np.cos(_angle)]
#     ])
#     return np.dot(points, rotation_matrix)
#
#
# def project(points):
#     """ Project 3D points to 2D using orthographic projection """
#     return points[:, :2]
#
#
# def draw_cube(points, projected_points):
#     # Calculate face depths using the original 3D points
#     face_depths = [(face, np.mean(points[face, 2])) for face in faces]
#     # Sort faces by depth
#     face_depths.sort(key=lambda x: x[1], reverse=True)
#
#     # Draw sorted faces using projected 2D points
#     for face, _ in face_depths:
#
#         polygon = [projected_points[i] for i in face]
#         pygame.draw.polygon(screen, (40, 60, 145), polygon, 0)
#         pygame.draw.polygon(screen, (0, 0, 0), polygon, 1)  # Draw black edges
#
#
# initial_rotation_y = np.radians(-30)
# initial_rotation_x = np.radians(35)
#
# running = True
# angle = 0
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_RIGHT:
#                 angle -= 0.1
#             elif event.key == pygame.K_LEFT:
#                 angle += 0.1
#             elif event.key == pygame.K_DOWN:
#                 initial_rotation_x += 0.1
#             elif event.key == pygame.K_UP:
#                 initial_rotation_x -= 0.1
#
#     screen.fill((50, 50, 50))
#
#     rotated_points = rotateY(cube_points, angle + initial_rotation_y)
#     rotated_points = rotateX(rotated_points, initial_rotation_x)
#     projected_points = project(rotated_points) * 100 + np.array([WIDTH // 2, HEIGHT // 2])
#
#     draw_cube(rotated_points, projected_points)
#
#     pygame.display.flip()
#
#     clock.tick(60)
#
# pygame.quit()
# sys.exit()
#=========================================================================
import pygame
import sys
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
# WIDTH, HEIGHT = 1439, 788
WIDTH, HEIGHT = 1200, 700

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cube with Lighting")

clock = pygame.time.Clock()

cube_points = np.array([
    [-1.5, -1.5, -1.5],
    [1.5, -1.5, -1.5],
    [1.5, 1.5, -1.5],
    [-1.5, 1.5, -1.5],
    [-1.5, -1.5, 1.5],
    [1.5, -1.5, 1.5],
    [1.5, 1.5, 1.5],
    [-1.5, 1.5, 1.5]
])

faces = [
    [0, 4, 5, 1],  # Front face
    [0, 1, 2, 3],  # Back face
    [0, 3, 7, 4],  # Top face
    [5, 4, 7, 6],  # Bottom face
    [1, 5, 6, 2],  # Right face
    [2, 6, 7, 3]  # Left face
]
#
colors = [
    (120, 120, 215),
    (120, 215, 120),
    (215, 120, 120),
    (120, 215, 215),
    (215, 120, 215),
    (215, 215, 120)
]

light_direction = np.array([-0.5, -0.5, -0.5])
light_direction = light_direction / np.linalg.norm(light_direction)  # Normalize the light vector


def rotateY(points, angle):
    rotation_matrix = np.array([
        [np.cos(angle), 0, np.sin(angle)],
        [0, 1, 0],
        [-np.sin(angle), 0, np.cos(angle)]
    ])
    return np.dot(points, rotation_matrix)


def rotateX(points, angle):
    rotation_matrix = np.array([
        [1, 0, 0],
        [0, np.cos(angle), -np.sin(angle)],
        [0, np.sin(angle), np.cos(angle)]
    ])
    return np.dot(points, rotation_matrix)


def project(points):
    return points[:, :2]


def face_normal(points, face):
    # Using three points from the face to calculate the normal
    v1 = points[face[1]] - points[face[0]]
    v2 = points[face[2]] - points[face[0]]
    return np.cross(v1, v2)


def calculate_light_intensity(normal, light_dir):
    # Normalize the face normal
    normal = normal / np.linalg.norm(normal)
    # Calculate the dot product
    return max(np.dot(normal, light_dir), 0)  # max to avoid negative values


def draw_cube(points, projected_points):
    face_depths = [(face, np.mean(points[face, 2])) for face in faces]
    face_depths.sort(key=lambda x: x[1], reverse=True)
    j = 0
    for face, _ in face_depths:
        normal = face_normal(points, face)
        intensity = calculate_light_intensity(normal, light_direction)
        base_color = (60, 80, 185)
        color = ( int(base_color[0] + 175 * intensity), int(base_color[1] + 155 * intensity), int(base_color[2] + intensity * 70))
    # for i, face in enumerate(faces):

        polygon = [projected_points[i] for i in face]
        # pygame.draw.polygon(screen, color, polygon, 0)
        pygame.draw.polygon(screen, colors[j], polygon, 0)  # Fill the polygon
        j += 1
        pygame.draw.polygon(screen, (0, 0, 0), polygon, 1)  # Draw black edges


initial_rotation_y = np.radians(-15)
initial_rotation_x = np.radians(20)

running = True
angle = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                angle += 0.1
            elif event.key == pygame.K_LEFT:
                angle -= 0.1
            elif event.key == pygame.K_DOWN:
                initial_rotation_x -= 0.1
            elif event.key == pygame.K_UP:
                initial_rotation_x += 0.1

    # screen.fill((50, 50, 50))
    screen.fill((20, 20, 25))

    rotated_points = rotateY(cube_points, angle + initial_rotation_y)
    rotated_points = rotateX(rotated_points, initial_rotation_x)
    projected_points = project(rotated_points) * 100 + np.array([WIDTH // 2, HEIGHT // 2])

    draw_cube(rotated_points, projected_points)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
