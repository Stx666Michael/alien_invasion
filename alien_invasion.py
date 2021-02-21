import pygame
from pygame.locals import *
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf
import time,threading

def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height),FULLSCREEN)
    pygame.display.set_caption("Alien Invation")
    pygame.mouse.set_visible(False)

    ship = Ship(ai_settings,screen)
    
    bullets = Group()
    bullet2s = Group()
    aliens = Group()
    deadaliens = Group()

    gf.create_an_alien(ai_settings,screen,aliens,deadaliens,bullet2s)
    threading.Timer(10,gf.create_an_alien2,(ai_settings,screen,aliens,deadaliens)).start()
    
    while True:
        a = time.time()
        gf.check_events(ai_settings,screen,ship,bullets)
        ship.update()
        gf.update_bullets(ai_settings,screen,ship,aliens,deadaliens,bullets)
        gf.update_bullet2s(ai_settings,screen,ship,aliens,deadaliens,bullet2s)
        gf.update_aliens(aliens)
        gf.update_screen(ai_settings,screen,ship,aliens,bullets,bullet2s)
        b = time.time()
        real_fps = 1/(b-a+1/ai_settings.FPS)
        ai_settings.set_speed(real_fps)
        pygame.time.Clock().tick(ai_settings.FPS)
           
run_game()

