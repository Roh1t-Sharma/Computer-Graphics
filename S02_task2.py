import pygame
import sys

pygame.init()

window_width, window_height = 800, 600

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Timed Circle Animation')

radius = 100
max_radius = window_width//2
change = 1
circle_color = (0, 255, 255)

clock = pygame.time.Clock()

def draw_circle(_radius):
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, circle_color, (window_width // 2, window_height // 2), _radius)
    pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    radius += change

    if radius <= 1 or radius >= max_radius:
        change = -change

    draw_circle(radius)

    clock.tick(30)

pygame.quit()
sys.exit()
