#Systematic explanation of collisions in pygame

#Pygame.rect represents rectangle with properties like (x,y,width,height)
#provides method to check for collisions between rectangles , such as colliderect

#create pygame.rect objects for entities you want to check for collisions, such
#as players , enemies , tiles.

# Example: Create a player rectangle
#player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

# Example: Create a tile rectangle
#tile_rect = pygame.Rect(tile_x, tile_y, tile_width, tile_height)

#use the colliderect method to check if rectangles collide
#if player_rect.colliderect(tile_rect):
    # Collision detected
    #print("Collision occurred!")

#this condition will be true if player_rect overlaps with tile_rect , indication a collision
#collision response
#if player_rect.colliderect(tile_rect):
    # Collision detected
    # Example: Stop player from moving further into the tile
    #if player_rect.right > tile_rect.left and player_rect.left < tile_rect.left:
      #  player_rect.right = tile_rect.left
    # Example: Adjust player's position vertically based on collision direction
    # (e.g., if player is falling and collides from below, stop falling)
    #elif player_rect.bottom > tile_rect.top and player_rect.top < tile_rect.top:
     #   player_rect.bottom = tile_rect.top

#Integrate collision detection 
#into your game loop where you update object positions and check for collisions each frame


#while running:
    # Handle user input, update player position, etc.
    
    # Example: Update player's rectangle based on position and size
    #player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    
    # Example: Check for collision with a tile
    #if player_rect.colliderect(tile_rect):
        # Implement collision response logic here
        # Adjust player's position, stop movement, etc.
    
    # Other game logic, drawing, updating, etc.
import pygame

# Initialize pygame
pygame.init()

# Game window setup
screen_width, screen_height = 800, 600
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Collision Detection Example")

# Player setup
player_x, player_y = 100, 100
player_width, player_height = 50, 50
player_color = (0, 255, 0)
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

# Tile setup
tile_x, tile_y = 300, 300
tile_width, tile_height = 100, 50
tile_color = (255, 0, 0)
tile_rect = pygame.Rect(tile_x, tile_y, tile_width, tile_height)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update player position (for example, based on user input)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= 1
    if keys[pygame.K_RIGHT]:
        player_x += 1
    if keys[pygame.K_UP]:
        player_y -= 1
    if keys[pygame.K_DOWN]:
        player_y += 1

    # Update player's rectangle
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    # Check for collision
    if player_rect.colliderect(tile_rect):
        # Handle collision response
        if player_rect.right > tile_rect.left and player_rect.left < tile_rect.left:
            player_x = tile_rect.left - player_width
        if player_rect.bottom > tile_rect.top and player_rect.top < tile_rect.top:
            player_y = tile_rect.top - player_height

    # Clear screen
    window.fill((255, 255, 255))

    # Draw player and tile
    pygame.draw.rect(window, player_color, player_rect)
    pygame.draw.rect(window, tile_color, tile_rect)

    # Update display
    pygame.display.flip()

# Quit pygame
pygame.quit()
