import pygame
import sys
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CUBE_COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (0, 255, 255),  # Cyan
    (255, 0, 255)   # Magenta
]

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RGB Cube")

background_image = pygame.image.load('/Users/rohitsharma/Downloads/6th Semester/Computer Graphics/Семинар 06/Пример/bitmap.bmp')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

clock = pygame.time.Clock()

cube_points = np.array([
    [1, 1, 1],
    [1, 1, -1],
    [1, -1, 1],
    [1, -1, -1],
    [-1, 1, 1],
    [-1, 1, -1],
    [-1, -1, 1],
    [-1, -1, -1]
])

# Define the faces using the vertices index
faces = [
    [0, 1, 3, 2], # Front face
    [4, 5, 7, 6], # Back face
    [0, 4, 6, 2], # Top face
    [1, 5, 7, 3], # Bottom face
    [0, 4, 5, 1], # Right face
    [2, 6, 7, 3]  # Left face
]

def rotateY(points, angle):
    """ Rotate the point around the Y axis by the given angle """
    rotation_matrix = np.array([
        [np.cos(angle), 0, np.sin(angle)],
        [0, 1, 0],
        [-np.sin(angle), 0, np.cos(angle)]
    ])
    return np.dot(points, rotation_matrix)

def rotateX(points, angle):
    """ Rotate the point around the X axis by the given angle """
    rotation_matrix = np.array([
        [1, 0, 0],
        [0, np.cos(angle), -np.sin(angle)],
        [0, np.sin(angle), np.cos(angle)]
    ])
    return np.dot(points, rotation_matrix)

def project(points):
    """ Project 3D points to 2D using orthographic projection """
    return points[:, :2]

def draw_cube(points):
    """ Draw the cube with colored faces """
    for i, face in enumerate(faces):
        polygon = [points[i] for i in face]
        pygame.draw.polygon(screen, CUBE_COLORS[i], polygon, 0)  # Fill the polygon

# Initial rotation for the cube to show three sides
initial_rotation_y = np.radians(-30)
initial_rotation_x = np.radians(35)

# Main loop
running = True
angle = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                angle -= 0.1
            elif event.key == pygame.K_RIGHT:
                angle += 0.1

    # Clear screen
    screen.blit(background_image, (0, 0))

    # Rotate the cube around Y axis and then X axis
    rotated_points = rotateY(cube_points, angle + initial_rotation_y)
    rotated_points = rotateX(rotated_points, initial_rotation_x)

    # Project the 3D points to 2D
    projected_points = project(rotated_points) * 100 + np.array([WIDTH // 2, HEIGHT // 2])

    # Draw the cube
    draw_cube(projected_points)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()