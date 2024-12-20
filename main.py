import os
import random
import math
import pygame
from pygame.locals import *
from EnemyTest import Enemy  # Import your Enemy class
from pygame import mixer
from abc import ABC, abstractmethod
from gameover import showdeath 
from Collectibles import Item
from Rhinoboss import Rhino
#import menu

pygame.mixer.init()

pygame.init()

pygame.display.set_caption("Spider-Man: The Video Game")

enemy_positions = []

# Constants
BG_COLOR = (255, 255, 255)
WIDTH, HEIGHT = 900, 600
FPS = 60
PLAYER_VEL = 5
WEBSWING_VEL = 15
KNOCKBACK_VEL =8
KNOCKBACK_RHINO = 30
GRAVITY = 1
JUMP_STRENGTH = 23
IDLE_WIDTH, IDLE_HEIGHT = 100, 100
JUMP_WIDTH, JUMP_HEIGHT = 90, 90
ATTACK_WIDTH, ATTACK_HEIGHT = 100, 100
RUN_WIDTH, RUN_HEIGHT = 100, 100
ELEVATOR_HEIGHT,ELEVATOR_WIDTH = 80,80
CLIMB_HEIGHT,CLIMB_WIDTH = 60,80
HURT_HEIGHT,HURT_WIDTH = 90,90
SWING_HEIGHT,SWING_WIDTH = 110,110
TILE_SIZE = 40
DOOR_WIDTH , DOOR_HEIGHT = 100,100

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

# Load images
player_img = pygame.image.load("Sprites/player.png")
jump_img = pygame.image.load("Sprites/jump.png")
attack_img = pygame.image.load("Sprites/punch1.png")
kick_img = pygame.image.load("Sprites/kick1.png")
run_img = pygame.image.load("Sprites/run.png")
climb_img = pygame.image.load("Sprites/climb.png")
playerhurt_img = pygame.image.load("Sprites/player_hurt.png")
webswing_img = pygame.image.load("Sprites/web_swing.png")
healthbar_img = pygame.image.load("Sprites/health bar.png")
bullet_img = pygame.image.load("Level Design/bullet.png")
background = pygame.image.load("backgrounds/Cityscape.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
ground_img = pygame.image.load("Level Design/Ground.png")
building_img = pygame.image.load("Level Design/buildings.png")
dialogue = pygame.image.load("Sprites/Spider-Man Talk.png")
dialogue_rect = dialogue.get_rect(topright=(100, 100))
door_img = pygame.image.load("Sprites/doorimage.png")
warp_point = pygame.image.load("Level Design/Elevator.png")

font = pygame.font.Font(None, 50)  # None for default font, 36 for font size
text = "Test!"
text_color = (0, 0, 0)  
text_surface = font.render(text, True, text_color)
text_rect = text_surface.get_rect(center=dialogue_rect.center)


# Blit the text onto the image
image_with_text = dialogue.copy()  # Create a copy of the image to modify
image_with_text.blit(text_surface, text_rect)  # Use topleft of text_rect to position text

# Scale images
player_img = pygame.transform.scale(player_img, (IDLE_WIDTH, IDLE_HEIGHT))
jump_img = pygame.transform.scale(jump_img, (JUMP_WIDTH, JUMP_HEIGHT))
attack_img = pygame.transform.scale(attack_img, (ATTACK_WIDTH, ATTACK_HEIGHT))
run_img = pygame.transform.scale(run_img, (RUN_WIDTH, RUN_HEIGHT))
warp_point = pygame.transform.scale(warp_point, (ELEVATOR_HEIGHT,ELEVATOR_WIDTH))
climb_img = pygame.transform.scale(climb_img, (CLIMB_HEIGHT, CLIMB_WIDTH))
playerhurt_img = pygame.transform.scale(playerhurt_img,(HURT_HEIGHT,HURT_WIDTH))
webswing_img = pygame.transform.scale(webswing_img, (SWING_HEIGHT,SWING_WIDTH))
door_img = pygame.transform.scale(door_img, (DOOR_HEIGHT, DOOR_WIDTH))



Web_soundeffect = pygame.mixer.Sound('Voicy_Spider-Man web shoot sound effect.mp3')
Punch_soundeffect = pygame.mixer.Sound('Punch Sound Effect.mp3')
jump_soundeffect = pygame.mixer.Sound('jump_11.wav')
collected_soundeffect = pygame.mixer.Sound('itemcollected.wav')

game_map = [
    ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '02', '0', '0', '0', '0', '0', '0'],
    ['1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '0', '0'],
    ['1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '1', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '0', '0'],
    ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
    ['1', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '0', '0'],
    ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '5', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
    ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0', '0', '2'],
    ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '3', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
    ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '4', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
    ['1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
    ['1', '0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
    ['1', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
    ['1', '0', '0', '0', '0', '0', '0', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0', '1', '1', '1', '1', '1', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
    ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
]

game_map2 = [
 ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
 ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
 ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
 ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
 ['1', '1', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0', '1', '1', '1', '1', '1', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1','0'],
 ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
 ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
 ['1', '0', '0', '5', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
 ['1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
 ['1', '1', '1', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0', '1', '1', '1', '1', '1', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1' ,'1'],
]

game_map3 = [
 ['0','0','0','0','0','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0', '0','0','0','0','1','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0', '0','0','0'],
 ['0','0','0','0','0','0','0','0','1','0', '0','0','0','0','0','0','0','0','0','0', '0','0','0','0','1','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0', '0','0','0'],
 ['0','0','0','0','0','0','0','0','1','0', '0','0','0','0','0','0','0','0','0','0', '1','0','0','0','1','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0', '0','0','0'],
 ['0','0','0','0','0','0','0','0','1','0', '0','0','0','0','0','0','0','0','0','0', '1','1','1','1','1','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0', '0','0','0','0','0','0','0',],
 ['0','0','0','0','0','0','0','0','1','0', '0','0','0','0','0','0','0','0','0','0', '1','0','0','0','1','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0', '0','0','0'],
 [ '0','0','0','0','0','0','0','0','1','0','0','0','0', '0','0','0','0','0','1','0','0','0','0', '0','0','0',],
 ['0','0','0','0','0','0','0','0','1','0', '0','0','0','0','0','0','0','0','0','0', '0','1','0','0','0','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0', '0','0','0'],
 ['0','0','0','0','0','0','0','0','1','0', '0','0','0','0','0','0','0','0','0','0', '0','1','0','0','1','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0', '0','0','0'],
 ['0','0','0','0','0','0','0','0','1','0', '0','0','0','0','0','0','0','0','1','0', '0','1','0','0','1','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0', '0','0','0'], 
 ['0','0','0','0','0','0','0','0','1','0', '0','0','0','0','0','5','0','0','1','0', '0','1','0','0','1','0','0','0','1','1', '1','1','1','1','1','1','1','1','1','1', '1','1','1','1','1','1','1','1','1','1','1','1','1','1','0','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0', '0','0','0'],
 ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1',]

]

maps = [game_map, game_map2 , game_map3]
global current_map_index
current_map_index = 0


# Set up display
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.vel_y = 0
        self.jumping = False
        self.health = 100
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_timer = 0
        self.attack_duration = FPS // 4  # Cooldown for 0.25 seconds
        self.idle = True
        self.num_of_attacks = 0
        self.facing_right = True
        self.climbing = False
        self.upside_down = False
        self.hurt = False
        self.hurt_timer = 2
        self.web_swing = 1
        self.swing = False
  
    def start_on_tile(self):
        for y, row in enumerate(game_map):
            for x, tile in enumerate(row):
                if tile == '1':
                    self.rect.x = x * TILE_SIZE
                    self.rect.y = (y * TILE_SIZE) - self.height

    def update(self, keys, tile_rects, enemies, items, Rhinos):
        global current_map_index
        dx = 0
        dy = 0
        self.walking = False

        # Handle horizontal movement
        if keys[pygame.K_LEFT]:
            dx -= PLAYER_VEL
            self.walking = True
            self.idle = False
            if self.facing_right:
                self.facing_right = False
                self.image = pygame.transform.flip(self.image, True, False)  # Flip image to face left
        if keys[pygame.K_RIGHT]:
            dx += PLAYER_VEL
            self.walking = True
            self.idle = False
            if not self.facing_right:
                self.facing_right = True
                self.image = pygame.transform.flip(self.image, True, False)  # Flip image to face right
       # if keys [pygame.K_1]:
        #    print("changing map!")
         #   global current_map_index
          #  current_map_index = (current_map_index + 1) % len(maps)
           # print(f"New map index: {current_map_index}")
            #self.start_on_tile()
  

        # Handle jumping
        if not self.jumping and keys[pygame.K_SPACE]:
            jump_soundeffect.play()
            self.jumping = True
            self.vel_y = -JUMP_STRENGTH
            self.idle = False
        if self.jumping and keys [pygame.K_w] and self.facing_right:
             self.swing = True
             dx += WEBSWING_VEL
             self.image = webswing_img
             Web_soundeffect.play()
        if self.jumping and keys [pygame.K_w] and not self.facing_right:
            self.swing = True
            dx -= WEBSWING_VEL
            self.image = webswing_img
            self.image = pygame.transform.flip(self.image, True, False)
            Web_soundeffect.play()
            
      
        if self.hurt:
            self.hurt_timer = -2
            self.image = playerhurt_img
            if self.hurt_timer <=0:
               self.hurt_timer = False
               self.idle = True
               self.hurt = False
               

        # Handle attacking
        if keys[pygame.K_s] or keys[pygame.K_d]:
            self.attack()
            self.idle = False
            colliding_enemy = pygame.sprite.spritecollideany(self, enemies)
            if colliding_enemy:
                Punch_soundeffect.play()
                self.combo(window)
                colliding_enemy.take_damage()
                self.num_of_attacks += 1
            colliding_attackrhino = pygame.sprite.spritecollideany(self, Rhinos)
            if colliding_attackrhino:
                Punch_soundeffect.play()
                colliding_attackrhino.take_rhino_damage()
                print("Rhino hurt!")

        if not keys[pygame.K_s] or keys[pygame.K_d]:
            colliding_enemy = pygame.sprite.spritecollideany(self, enemies)
            if colliding_enemy:
                 print ("attack stance detected")
                 colliding_enemy.attack_stance()
                 dx -= KNOCKBACK_VEL
                 self.health -= 1 
                 print ("player hurt!")
                 self.hurt = True
                 
                 if self.health <= 0:
                        self.kill()
                        pygame.mixer_music.stop()
                        showdeath()
                       

        colliding_collectibles = pygame.sprite.spritecollideany(self, items)
        if colliding_collectibles:
            print("collectible collected!")
            colliding_collectibles.collected()
            collected_soundeffect.play()


        colliding_rhino = pygame.sprite.spritecollideany(self,Rhinos)
        if colliding_rhino:
            print("Rhino collision!")
          #  dx -= KNOCKBACK_RHINO
            Punch_soundeffect.play()
            self.hurt = True
            



                        
        def kill(self):
        # Logic to remove the player from the game or sprite group
            pass

                             
        if self.attack_timer > 0:
            self.attack_timer -= 1
            if self.attack_timer == 0:
                self.is_attacking = False

        # Apply gravity
        if self.jumping and self.facing_right and not keys[pygame.K_w]:
            self.vel_y += GRAVITY
            dy += self.vel_y
            self.image = jump_img
        if self.jumping and not self.facing_right and not keys[pygame.K_w]:
            self.vel_y += GRAVITY
            dy += self.vel_y
            self.image = pygame.transform.flip(jump_img, True , False)
   
        # Check for collisions in x direction
        self.rect.x += dx
        for tile_rect in tile_rects:
            if self.rect.colliderect(tile_rect):
                print("colliding with wall")
                if dx > 0:  # Moving right; adjust position
                    self.rect.right = tile_rect.left
                    self.idle = False
                    if keys [pygame.K_q]:
                        self.image = climb_img
                        self.climbing = True
                elif dx < 0:  # Moving left; adjust position
                    self.rect.left = tile_rect.right
                    self.idle = False
                    if keys [pygame.K_q]:
                         self.idle = False
                         self.walking = False
                         self.climbing = True
          # Handle climbing
        if self.climbing : 
            self.walking == False
            print("climbing")
            self.vel_y = 0  # Stop falling
            if keys[pygame.K_UP] and self.facing_right:
                self.image = climb_img
                dy -= PLAYER_VEL 
            if keys[pygame.K_UP] and not self.facing_right:
                self.image = pygame.transform.flip(climb_img, True , False)
                dy -= PLAYER_VEL
               

            elif keys[pygame.K_DOWN]:
                self.image = climb_img
                dy += PLAYER_VEL
            else:
                self.climbing = False  # Stop climbing if no movement
                         

        # Check for collisions in y direction
        self.rect.y += dy
        on_ground = False
        for tile_rect in tile_rects:
            if self.rect.colliderect(tile_rect):
                if dy > 0:  # Falling
                    self.rect.bottom = tile_rect.top
                    self.jumping = False
                    self.vel_y = 0
                    on_ground = True
                    self.idle = False
                elif dy < 0:  # Jumping
                    self.rect.top = tile_rect.bottom
                    self.vel_y = 0
                    self.idle = False
                    if keys [pygame.K_q]:
                        not self.walking
                        self.upside_down = True

        # If not on ground and not colliding with any tile below, continue falling
        if not on_ground:
            self.jumping = True
            self.idle = False

        # Determine idle state
        if on_ground and not self.walking and not self.is_attacking and not self.jumping:
            self.idle = True
        else:
            self.idle = False


        if self.is_attacking:
            self.image = attack_img
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)
        elif self.walking:
            self.image = run_img
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)
        elif self.idle:
            self.image = player_img
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

        # Handle attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.scroll = [0,0]

    def attack(self):
        if self.attack_cooldown == 0 and not self.is_attacking:
            self.is_attacking = True
            self.attack_timer = self.attack_duration
            self.attack_cooldown = FPS // 4  # Cooldown for 0.25 seconds

    def combo(self, window):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(f'Combo X{self.num_of_attacks}', True, green, blue)
        textRect = text.get_rect()
        textRect.right = WIDTH - 10  # 10 pixels from the right edge
        textRect.top = 10
        window.blit(text, textRect)

    def draw_healthbar(self, window):
        window.blit(healthbar_img, (0, 0))

class Camera:
    def __init__(self, width , height):
        self.camera = pygame.Rect(0,0,width,height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)
    
    def reverse_apply(self, pos):
        x, y = pos
        return (x - self.camera.topleft[0], y - self.camera.topleft[1])

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # Limit scrolling to map size
        x = min(0, x)  # Left edge
        y = min(0, y)  # Top edge
        x = max(-(self.width - WIDTH), x)  # Right edge
        y = max(-(self.height - HEIGHT), y)  # Bottom edge

        self.camera = pygame.Rect(x, y, self.width, self.height)
        

def initialize_enemies(current_map_index):
    global enemy_positions
    enemy_positions.clear()
    if current_map_index == 0:
        print("current map index is 0")
        enemy_positions = [
        (600,260),
        (200,260),      
        ]
    elif current_map_index == 1:
        print("current map index is 1")
        enemy_positions = [(300,270)]
    elif current_map_index == 2:
        print("current map index is 2")
        enemy_positions = []
    else:
        enemy_positions = []

def create_items(current_map_index):
    global items_positions
    items_positions = []
    if current_map_index == 0:
        print("current map index is 0")
        items_positions = [
        (100,710),
           
        ]
    elif current_map_index == 1:
        print("current map index is 1")
        items_positions = []
    elif current_map_index == 2:
        print("current map index is 2")
        items_positions = []
    else:
        items_positions = []

def initialize_rhino(current_map_index):
    global rhino_position
    rhino_position=[]

    if current_map_index == 2:
        # Set the position(s) for the rhino
        rhino_position = [(1500, 250)]  # Example position, adjust as needed
        print("Rhino initialized at map 2")
        
    
def main(window):
    global current_map_index

    # Initialize enemy positions based on the current map index
    initialize_enemies(current_map_index)
    create_items(current_map_index)
    initialize_rhino(current_map_index)

    dx = 0
    dy = 0

    player = Player()
  

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
   

    enemies = pygame.sprite.Group()

    items = pygame.sprite.Group()

    Rhinos = pygame.sprite.Group()

    for pos in items_positions:
        x,y = pos
        item = Item(x,y)
        items.add(item)


    for pos in enemy_positions:
        x , y = pos
        enemy = Enemy(x,y)
        enemies.add(enemy)

    for pos in rhino_position:
        x,y = pos   
        rhino = Rhino(x,y)
        Rhinos.add(rhino)
       

    # Create a camera instance
    camera = Camera(len(game_map[0]) * TILE_SIZE, len(game_map) * TILE_SIZE)

    pygame.mixer.music.load('06 Stop The Bomb.mp3')
    pygame.mixer.music.play(-1) 
    
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = camera.reverse_apply(event.pos)
                print(f"Mouse clicked at {event.pos}") 

                for inflated_rects in inflated_transported_rects:
                     if inflated_rects.collidepoint((mouse_x,mouse_y)):  
                      print("door detected")
                      current_map_index = (current_map_index + 1) % len(maps)
                      enemy_positions.clear()  
                      items_positions.clear()
                      rhino_position.clear()  
                
                      initialize_enemies(current_map_index)
                      initialize_rhino(current_map_index)
                      create_items(current_map_index)
                      enemies.empty()
                      Rhinos.empty()
                       


                      for pos in enemy_positions:
                          x, y = pos
                          enemy = Enemy(x, y)
                          enemies.add(enemy)
                      for pos in rhino_position:
                          x, y = pos
                          rhino = Rhino(x, y)
                          Rhinos.add(rhino)
 
        keys = pygame.key.get_pressed()

        # Draw the background
        window.blit(background, (0, 0))

      
        
         
        # Draw the tiles with camera offset
        tile_rects = []
        tile_types = []
        enemy_rects = []
        transport_rects = []
        inflated_transported_rects = []
        y = 0
        for row in maps[current_map_index]:
            x = 0
            for tile in row:
                if tile == '1':
                    tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    tile_rects.append(tile_rect)
                    tile_types.append('1')
                    # Apply camera to tile position
                    window.blit(ground_img, camera.apply_rect(tile_rect))
                    # Draw tile collision box
                    #pygame.draw.rect(window, (255, 0, 0), camera.apply_rect(tile_rect), 2)
                if tile == '2':
                    tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    tile_rects.append(tile_rect)
                    tile_types.append('2')
                    # Apply camera to tile position
                    window.blit(building_img, camera.apply_rect(tile_rect))
                if tile == '3':
                    tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    window.blit(warp_point, camera.apply_rect(tile_rect))
                    tile_types.append('3')
                if tile == '5':
                    transport_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    transport_rects.append(transport_rect)
                    tile_types.append('5')
                    

                     # Inflate the rect for a larger collision box
                    inflated_rect = transport_rect.inflate(100, 100)  # Increase size by 20 pixels
            
                    # Add the inflated rect for collision checks, not for drawing
                    inflated_transported_rects.append(inflated_rect)
            
                    window.blit(door_img, camera.apply_rect(inflated_rect))
                   # pygame.draw.rect(window, (255, 0, 0), camera.apply_rect(inflated_rect), 2)


                 
                    

                x += 1
            y += 1


       
        # Update player with tile_rects
        player.update(keys, tile_rects, enemies, items, Rhinos)

      #  pygame.draw.rect(window, (0, 255, 0), camera.apply_rect(player.rect))

        enemy.update()

        Rhinos.update()
        
        
       # change_map()

        # Update the camera to follow the player
        camera.update(player)

        # Draw the player and other sprites with camera offset
        for sprite in all_sprites:
            window.blit(sprite.image, camera.apply(sprite))
        
        for item in items:
            window.blit(item.image,camera.apply(item))
        
        for rhino in Rhinos:
          if current_map_index == 2:
            #window.blit(rhino.image, (200, 260)) 
            window.blit(rhino.image, camera.apply(rhino))
            rhino.draw_rhino_health(window)

           # print(f"Drawing Rhino at: {rhino.rect.topleft}")
           #  window.blit(rhino.image,camera.apply(rhino))
           # pygame.draw.rect(window, (255, 0, 0), camera.apply_rect(rhino.rect), 2)  # Draw debug rect
           # print(f"Rhino rect: {rhino.rect}")


     
        for enemy in enemies:
            enemy.vel_y += GRAVITY
            dy += enemy.vel_y
            window.blit(enemy.image, camera.apply(enemy))
            enemy.rect.x += dx
            for tile_rect in tile_rects:
             if enemy.rect.colliderect(tile_rect):
                if dx > 0:  # Moving right; adjust position
                    enemy.rect.right = tile_rect.left
                    enemy.idle = False
                elif dx < 0:  # Moving left; adjust position
                    enemy.rect.left = tile_rect.right
                    enemy.idle = False

        # Draw the health bar
        player.draw_healthbar(window)

        # Update the display
        pygame.display.flip()

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)
