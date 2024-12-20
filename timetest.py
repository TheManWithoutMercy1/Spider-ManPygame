import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame get_ticks Example")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the number of milliseconds since Pygame was initialized
    ticks = pygame.time.get_ticks()

    # Convert milliseconds to seconds
    seconds = ticks / 1000

    # Print the elapsed time
    print(f"Time elapsed: {seconds:.2f} seconds")

    # Fill the screen with a color
    screen.fill((0, 0, 0))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
