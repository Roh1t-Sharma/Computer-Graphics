import pygame
import math
from pygame.locals import *


def bresenham_line(surface, x1, y1, x2, y2, color):
    dx = abs(x2 - x1)
    dy = -abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx + dy
    while True:
        surface.set_at((x1, y1), color)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x1 += sx
        if e2 <= dx:
            err += dx
            y1 += sy


# Function to draw figures
def draw_figure(surface, center_x, center_y, rect_width, rect_height, triangle_height, ra_triangle_height, angle, dx, dy):

    # rect_color = (0, 128, 255)
    # iso_triangle_color = (51, 51, 255)
    # ra_triangle_color = (178, 102, 255)

    rect_color = (0, 0, 0)
    iso_triangle_color = (190, 0, 0)
    ra_triangle_color = (150, 150, 150)

    rect_points = [
        (center_x - rect_width // 2, center_y),
        (center_x + rect_width // 2, center_y),
        (center_x + rect_width // 2, center_y + rect_height),
        (center_x - rect_width // 2, center_y + rect_height),
    ]

    iso_tri_points = [
        (center_x - rect_width // 4 - rect_width // 4, center_y),
        (center_x + rect_width // 4 - rect_width // 4, center_y),
        (center_x - rect_width // 4, center_y - triangle_height),
    ]

    line_points = [
        (center_x + rect_width // 2, center_y + rect_height // 2),
        (center_x + rect_width // 2 + 20, center_y + rect_height // 2),
    ]

    ra_tri_points = [
        (line_points[1][0], line_points[1][1] - ra_triangle_height // 2),
        (line_points[1][0], line_points[1][1] + ra_triangle_height // 2),
        (line_points[1][0] + ra_triangle_height // 2, line_points[1][1] + ra_triangle_height // 2)
    ]

    all_points = rect_points + iso_tri_points + line_points + ra_tri_points
    transformed_points = []
    for x, y in all_points:
        x -= center_x
        y -= center_y
        # Apply rotation
        x_new = x * math.cos(angle) - y * math.sin(angle)
        y_new = x * math.sin(angle) + y * math.cos(angle)

        x_new += center_x + dx
        y_new += center_y + dy
        transformed_points.append((int(x_new), int(y_new)))

    t_rect_points = transformed_points[:4]
    t_iso_tri_points = transformed_points[4:7]
    t_line_points = transformed_points[7:9]
    t_ra_tri_points = transformed_points[9:12]

    BLACK = (0, 0, 0)

    pygame.draw.polygon(surface, rect_color, t_rect_points)
    pygame.draw.polygon(surface, iso_triangle_color, t_iso_tri_points)
    pygame.draw.lines(surface, BLACK, False, t_line_points, 1)
    pygame.draw.polygon(surface, ra_triangle_color, t_ra_tri_points)

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Cube')

WHITE = (255, 255, 255)

rect_width, rect_height = 200, 100
triangle_height = 50
ra_triangle_height = 100

center_x, center_y = width // 2, height // 2

angle = 0
dx, dy = 0, 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click - rotate
                angle += math.radians(10)
            elif event.button == 3:  # Right click - move
                dx, dy = event.pos[0] - center_x, event.pos[1] - center_y

    buffer = pygame.Surface((width, height))
    buffer.fill(WHITE)

    draw_figure(buffer, center_x, center_y, rect_width, rect_height, triangle_height, ra_triangle_height, angle, dx,
                dy)

    screen.blit(buffer, (0, 0))
    pygame.display.flip()


pygame.quit()
