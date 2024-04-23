import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants for the display
WIDTH, HEIGHT = 900, 700
BACKGROUND_COLOR = (0, 100, 0)  # White

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Snoop = Snooporate")
# pygame.display.set_caption("Ratorate")

# Clock for controlling frame rate
clock = pygame.time.Clock()

image = pygame.image.load('/Users/rohitsharma/Downloads/snoop.png')
pygame.mixer.init()
pygame.mixer.music.load('/Users/rohitsharma/Downloads/smoke.mp3')
pygame.mixer.music.play(-1)
image_rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Angle of rotation
angle = 0

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill(BACKGROUND_COLOR)

    # Rotate the image
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image_rect.center)  # Ensure the image rotates around its center

    # Draw the image
    screen.blit(rotated_image, new_rect.topleft)

    # Update display
    pygame.display.flip()

    # Increase the angle for the next frame
    angle -= 1  # Rotate 1 degree per frame counterclockwise

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
