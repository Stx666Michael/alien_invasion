import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self,ai_settings,screen,ship):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('images/love1.png')       
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.centery = ship.rect.centery
        
        self.initial_speed_1 = ai_settings.screen_height
        self.initial_speed_2 = ai_settings.screen_width
        self.initial_1 = ship.rect.bottom
        self.initial_2 = ship.rect.top
        self.initial_3 = ship.rect.right
        self.initial_4 = ship.rect.left

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.speed_factor = ai_settings.bullet_speed_factor

        self.shooting_up = False
        self.shooting_down = False
        self.shooting_left = False
        self.shooting_right = False
        
    def position(self,ship):
        if self.shooting_up:
            self.y -= (ship.rect.height-self.rect.height)/2

        elif self.shooting_down:
            self.y += (ship.rect.height-self.rect.height)/2

        elif self.shooting_left:
            self.x -= (ship.rect.width-self.rect.width)/2

        elif self.shooting_right:
            self.x += (ship.rect.width-self.rect.width)/2

    def update(self):
        if self.shooting_up:
            self.y -= abs(self.speed_factor*((self.initial_speed_1-self.initial_1+self.y+self.rect.height)/90)**(1/2))

        elif self.shooting_down:
            self.y += abs(self.speed_factor*((self.initial_speed_1+self.initial_2-self.y+self.rect.height)/90)**(1/2))

        elif self.shooting_left:
            self.x -= abs(self.speed_factor*((self.initial_speed_2-self.initial_3+self.x+self.rect.width)/160)**(1/2))

        elif self.shooting_right:
            self.x += abs(self.speed_factor*((self.initial_speed_2+self.initial_4-self.x+self.rect.width)/160)**(1/2))
            
        self.rect.y = self.y
        self.rect.x = self.x
        
    def draw_bullet(self):
        self.screen.blit(self.image,self.rect)
