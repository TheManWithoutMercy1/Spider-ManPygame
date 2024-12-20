from typing import Any
import pygame


rhino_img = pygame.image.load('Sprites/rhino.png')
rhinodash = pygame.image.load('Sprites/rhinorun.png')
rhinotired = pygame.image.load('Sprites/rhino_tired.png')
rhinohurt = pygame.image.load('Sprites/rhino_hurt.png')
rhinohealth = pygame.image.load('Sprites/rhinohealthbar.png')


import pygame

# Load the images (assuming they're properly loaded elsewhere in your main game code)
rhino_img = pygame.image.load('Sprites/rhino.png')
rhinodash = pygame.image.load('Sprites/rhinorun.png')
rhinodash2 = pygame.image.load('Sprites/rhinorun2.png')
rhinotired = pygame.image.load('Sprites/rhino_tired.png')
rhinohurt = pygame.image.load('Sprites/rhino_hurt.png')
rhinohealth = pygame.image.load('Sprites/rhinohealthbar.png')

class Rhino(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = rhino_img
        self.dash_img = rhinodash
        self.dash2_img = rhinodash2
        self.tired_img = rhinotired
        self.hurt_img = rhinohurt

        # Set the initial position using arguments
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # Rhino states
        self.idle = True
        self.hurt = False
        self.dash = False
        self.tired = False
        self.vulnerable = False
        
        # Rhino properties
        self.health = 1000
        self.start_time = pygame.time.get_ticks()
        self.dx = 5  # movement speed if needed for dashing, etc.
        self.hurt_timer = 0
        self.hurt_duration = 250
        self.facing_left = True
        self.facing_right = False

    def rhino_draw(self, window):
        # Check Rhino states and draw the appropriate image
        if self.hurt:
            window.blit(self.hurt_img, self.rect)
        elif self.tired:
            window.blit(self.tired_img, self.rect)
        elif self.dash:
            window.blit(self.dash_img, self.rect)
        else:
            window.blit(self.image, self.rect)
        if self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False) 
            window.blit(self.image, self.rect)
    
    def draw_rhino_health(self,window):
        window.blit(rhinohealth, (400,10))

    def take_rhino_damage(self):
        self.hurt = True
        self.health -= 2
        self.hurt_timer = pygame.time.get_ticks()
        if self.health <= 0:
            self.kill()
    

    def update(self):
     
     
     current_time = pygame.time.get_ticks()

     if self.hurt:
         self.image = self.hurt_img
         current_time = pygame.time.get_ticks()
         if current_time - self.hurt_timer >= self.hurt_duration:
          self.hurt = False  # Reset hurt state
          self.dash = True
          #self.image = rhino_img  # Revert to the normal image
            
     if self.dash:
         elapsed_time = (current_time - self.start_time) % 2000  
         if elapsed_time < 1000:
            self.image = self.dash_img
            dx = 10
            self.rect.x -= dx
         else:
            self.image = self.dash2_img
            self.facing_right = True
            dx = 10
            self.rect.x += dx

    def drawbox_rhino(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.rect, 2)


        





    


        



