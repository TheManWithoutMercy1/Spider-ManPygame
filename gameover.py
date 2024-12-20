import pygame
from pygame.locals import *
from pygame import mixer

# Load the death screen image
death_img = pygame.image.load("backgrounds/spider-man death.png")
death_img = pygame.transform.scale(death_img, (800, 600))


class Death:
    def __init__(self):
        self.run = True  # Control the loop
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Death Screen")

    def run_death_screen(self):
        clock = pygame.time.Clock()
        
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False  # Stop the loop on quit event

            # Blit the death image onto the screen
            self.screen.blit(death_img, (0, 0))

            # Update the display
            pygame.display.flip()

            # Control the frame rate (60 FPS)
            clock.tick(60)

            pygame.mixer_music.load('death_screen.mp3')
            pygame.mixer_music.play()





def showdeath():
    death_screen = Death()  # Create an instance of Death
    death_screen.run_death_screen()  # Run the death screen loop


      
