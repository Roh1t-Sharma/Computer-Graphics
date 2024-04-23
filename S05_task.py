import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
QUAD_COLOR = (0, 128, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Quadrilateral")

clock = pygame.time.Clock()

points = [
    (300, 200),
    (500, 200),
    (550, 400),
    (250, 400)
]


def rotate_point(cx, cy, _angle, px, py):
    """ Rotate a point around a given center. """
    s = math.sin(_angle)
    c = math.cos(_angle)

    # Translate point to origin
    px -= cx
    py -= cy

    # Rotate point
    xnew = px * c - py * s
    ynew = px * s + py * c

    # Translate point back
    px = xnew + cx
    py = ynew + cy
    return px, py


def rotate_shape(_points, _angle):
    """ to rotate the shape around the center of the screen. """
    cx, cy = WIDTH // 2, HEIGHT // 2
    return [rotate_point(cx, cy, _angle, px, py) for px, py in _points]


# Angle of rotation in radians
angle = 0

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)

    # Rotate the shape
    rotated_points = rotate_shape(points, angle)
    pygame.draw.polygon(screen, QUAD_COLOR, rotated_points)

    # Update display
    pygame.display.flip()

    # Increase the angle for the next frame
    angle += math.radians(1)  # Rotate 1 degree per frame

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
