import pygame
from pygame.sprite import Sprite

class Bullet2(Sprite):
    def __init__(self,ai_settings,screen,alien):
        super().__init__()
        self.screen = screen

        self.image = pygame.image.load('images/love1.png')       
        self.rect = self.image.get_rect()
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom

        self.y = float(self.rect.y)
        self.speed_factor = ai_settings.bullet_speed_factor
        self.dead_y = alien.dead_y

    def update(self):
        self.y += self.speed_factor*((self.y-self.dead_y)/100)**(1/2)
        self.rect.y = self.y        

    def draw_bullet(self):
        self.screen.blit(self.image,self.rect)
