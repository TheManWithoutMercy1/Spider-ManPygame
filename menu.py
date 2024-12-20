import pygame
from pygame.locals import *
from pygame import mixer
import main

pygame.init()

menu_img = pygame.image.load("backgrounds/menu screen.png")
menu_img2 = pygame.transform.scale(menu_img,((800,600)))

start_img = pygame.image.load("Sprites/start.png")
exit_img = pygame.image.load("Sprites/exit.png")

mixer.music.load('02 Title Screen.mp3')
mixer.music.play(-1)

class Menu:
   def __init__(self):
    self.screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Main Menu")
    self.run = True
      
   def updatemainmenu(self):
    while self.run:
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self.run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
               if start_button.collidepoint(event.pos):
                  print("mouse detected")
                  main.main(main.window)


            if event.type == pygame.MOUSEBUTTONDOWN:
               if exit_button.collidepoint(event.pos):
                  self.run = False
            

         self.screen.blit(menu_img2, (0,0))
         start_button.draw(self.screen)
         exit_button.draw(self.screen)
         pygame.display.flip()

class Buttons:
    def __init__(self,image,x,y):
      self.image = image
      self.rect = self.image.get_rect()
      self.rect.topleft = (x,y)

    def draw(self, screen):
     screen.blit(self.image, (self.rect.x, self.rect.y))

    def collidepoint(self,pos):
        return self.rect.collidepoint(pos)

start_button = Buttons(start_img,450,250)
exit_button = Buttons(exit_img,450,300)
       
#def showmenu():
menu_screen = Menu()
menu_screen.updatemainmenu()

pygame.quit()

