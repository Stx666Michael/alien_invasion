import pygame
from pygame.sprite import Sprite
from random import *

class Alien(Sprite):
    def __init__(self,ai_settings,screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('images/xhh1.png')       
        self.rect = self.image.get_rect()

        self.rect.x = ai_settings.screen_width*(randint(1,4)/5)
        self.rect.y = self.rect.height/2
        self.dead_y = 0
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.direction = choice([-1,1])
        self.direction_y = 1

        self.alien_kind = 2

        self.healthy = True

    def blitme(self):
        self.screen.blit(self.image,self.rect)
    
    def update(self):
        if self.alien_kind == 1:
            self.x += self.ai_settings.alien_speed_factor*self.direction
            self.y += self.ai_settings.alien_speed_factor_y*self.direction_y

        elif self.alien_kind == 2:
            self.x += self.ai_settings.alien_speed_factor*(((abs(self.x-self.ai_settings.screen_width/2)+1)/100)**(1/2))*self.direction
            self.y += self.ai_settings.alien_speed_factor_y*self.direction_y

        elif self.alien_kind == 3:
            self.x += self.ai_settings.alien_speed_factor*self.direction/2
            if self.healthy:
                self.y += self.ai_settings.alien_speed_factor*((abs(self.y-self.rect.height/2)/50)**(1/2))*self.direction_y            
                if self.y <= self.rect.height/2:
                    self.direction_y *= -1
                   
        self.rect.x = self.x     
        self.rect.y = self.y
       
