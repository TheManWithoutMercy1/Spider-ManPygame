import pygame

blacksuit_img = pygame.image.load("Sprites/symbiotecollectible.png")
blacksuit_img = pygame.transform.scale(blacksuit_img,(50,50))

class Item(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__() 
        self.image = blacksuit_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.count = 0

   
    def draw(self,window):
        window.blit(self.image)

    def collected(self):
        self.kill()
        self.count += 1


    def drawbox(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.rect, 2)