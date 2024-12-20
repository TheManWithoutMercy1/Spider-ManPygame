import pygame
import math

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRAVITY = 0.5
WEB_LENGTH = 200  # The maximum length of the web

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics-based Web Swinging")

# Player properties
player_pos = [400, 300]
player_radius = 20
player_velocity = [0, 0]

# Web properties
web_attached = False
web_anchor = [400, 100]
web_length = WEB_LENGTH

clock = pygame.time.Clock()

def apply_gravity(velocity):
    velocity[1] += GRAVITY
    return velocity

def constrain_to_web(player_pos, web_anchor, web_length):
    dx = player_pos[0] - web_anchor[0]
    dy = player_pos[1] - web_anchor[1]
    distance = math.sqrt(dx**2 + dy**2)
    
    if distance > web_length:
        angle = math.atan2(dy, dx)
        player_pos[0] = web_anchor[0] + web_length * math.cos(angle)
        player_pos[1] = web_anchor[1] + web_length * math.sin(angle)
    return player_pos

def swinging_motion(player_pos, player_velocity, web_anchor):
    dx = player_pos[0] - web_anchor[0]
    dy = player_pos[1] - web_anchor[1]
    angle = math.atan2(dy, dx)
    tension_force = 0.01 * angle  # Small force for swinging
    
    player_velocity[0] -= tension_force * math.sin(angle)
    player_velocity[1] += tension_force * math.cos(angle)

    return player_velocity

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            web_attached = True
            web_anchor = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP:
            web_attached = False

    # Apply gravity
    player_velocity = apply_gravity(player_velocity)

    # Update player's position
    player_pos[0] += player_velocity[0]
    player_pos[1] += player_velocity[1]

    # Constrain the player to the web if attached
    if web_attached:
        player_pos = constrain_to_web(player_pos, web_anchor, web_length)

    # Apply swinging motion if web is attached
    if web_attached:
        player_velocity = swinging_motion(player_pos, player_velocity, web_anchor)

    # Drawing the player and the web
    screen.fill((0, 0, 0))

    if web_attached:
        pygame.draw.line(screen, (255, 255, 255), web_anchor, player_pos, 2)

    pygame.draw.circle(screen, (0, 255, 0), (int(player_pos[0]), int(player_pos[1])), player_radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
