import pygame
import sys

# Initialize the pygame
pygame.init()

# Set the dimensions of the window
window_width, window_height = 800, 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Circle Radius Control')

# Set the initial radius of the circle
radius = 150

# The color of the circle
circle_color = (0, 255, 0)

# Clock to control the frames per second
clock = pygame.time.Clock()


# Function to draw the circle in the center of the window
def draw_circle(_radius):
    screen.fill((0, 0, 0))  # Fill the screen with black background
    pygame.draw.circle(screen, circle_color, (window_width // 2, window_height // 2), _radius)
    pygame.display.flip()


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        # Increase the radius, ensuring it does not exceed half the window width
        if radius < window_width // 2:
            radius += 1
    elif keys[pygame.K_LEFT]:
        # Decrease the radius, ensuring it does not go below 1
        if radius > 1:
            radius -= 1

    draw_circle(radius)

    # Limit the loop to 30 times per second
    clock.tick(30)

# Quit the game
pygame.quit()
sys.exit()
