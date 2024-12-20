#Enemy A.I implementation
#step by step
#1.render the sprite
#2.implement collision
#3.add idle state
#4.add combat state
#5.add hurt state
import pygame

ENEMY_VEL = 2
IDLE_VEL = 0
WAIT_TIME = 60
BULLET_VEL = 5

CARNAGE_WIDTH, CARNAGE_HEIGHT = 100,100
idle_img = pygame.image.load("Sprites/enemystrike.png")
bullet_img = pygame.image.load("Level Design/bullet.png")
hurt_img = pygame.image.load("Sprites/enemy_soldier_hurt.png")
attack_img = pygame.image.load("Sprites/enemy_soldier.png")
idle_img = pygame.transform.scale(idle_img, (CARNAGE_HEIGHT,CARNAGE_WIDTH))
hurt_img = pygame.transform.scale(hurt_img,  (CARNAGE_HEIGHT,CARNAGE_WIDTH))
idle2_img = pygame.transform.flip(idle_img , True, False)

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.x = 5
        self.y = 5
        self.vel_y = 0
        self.image = idle_img
        self.hurt_image = hurt_img
        self.attack_img = attack_img
        self.rect = self.image.get_rect()
        self.health = 45
        self.rect.topleft = (x,y)
        self.hurt = False
        self.move_right = False
        self.wait_timer = 0
        self.wait_duration = WAIT_TIME 
        self.start_time = pygame.time.get_ticks()
        self.direction = 1
        self.idle_state = True
        self.attacking = False
        self.hurt_timer = 0
        self.hurt_duration = 1
        dx = 1
        self.attack_stance_active = False
        self.attack_stance_timer = 1

    def draw(self, window):
     
      if  self.hurt:
        window.blit(self.hurt_image, self.rect)
      elif self.attack_stance_active:
        window.blit(self.attack_img,self.rect)
      else:
        window.blit(self.image, self.rect)

    def take_damage(self):
      self.health -= 1
      self.hurt = True
      if self.health <=0:
         self.kill()

    def attack_stance(self):
      
       self.hurt = False
       self.idle_state = False
       self.attack_stance_active = True


    def update(self):
     
      current_time = pygame.time.get_ticks()


      if self.attack_stance_active:
         self.attack_stance_timer -= 1
         dx = IDLE_VEL
         self.image = self.attack_img
         if self.attack_stance_timer <=0:
               self.attack_stance_active = False
               self.start_time = pygame.time.get_ticks()
     
      if  self.hurt:
         self.hurt_timer -= 1
         self.image = hurt_img
         dx = IDLE_VEL
         if self.hurt_timer <= 0:
            self.hurt = False
            self.start_time = pygame.time.get_ticks()  # Reset the timer
     
      else:
             if self.idle_state:
              elapsed_time = (current_time - self.start_time) % 2000  # Cycle every 2 seconds (2000 milliseconds)
            
              if elapsed_time < 1000:  # Move left for the first 1 second
                self.image = idle_img
                dx = ENEMY_VEL
                self.rect.x -= dx
              else:  # Move right for the next 1 second
                self.image = idle2_img
                dx = ENEMY_VEL
                self.rect.x += dx

        # Else, do nothing after 
    def drawbox(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.rect, 2)



        



