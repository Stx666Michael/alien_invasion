import sys
import pygame
from bullet import Bullet
from bullet2 import Bullet2
from alien import Alien
from random import uniform
import threading

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    if event.key == pygame.K_d:
        ship.moving_right = True        

    elif event.key == pygame.K_a:
        ship.moving_left = True

    elif event.key == pygame.K_w:
        ship.moving_up = True        

    elif event.key == pygame.K_s:
        ship.moving_down = True

    if ship.healthy:
        if event.key == pygame.K_UP:
            fire_bullet(ai_settings,screen,ship,bullets,'up')
            ship.image = pygame.image.load('images/xbb1.png')

        elif event.key == pygame.K_DOWN:
            fire_bullet(ai_settings,screen,ship,bullets,'down')
            ship.image = pygame.image.load('images/xbb1.png')

        elif event.key == pygame.K_LEFT:
            fire_bullet(ai_settings,screen,ship,bullets,'left')
            ship.image = pygame.image.load('images/xbb1.png')

        elif event.key == pygame.K_RIGHT:
            fire_bullet(ai_settings,screen,ship,bullets,'right')
            ship.image = pygame.image.load('images/xbb1.png')

    if not ship.healthy:
        if event.key == pygame.K_d:
            ship.image = pygame.image.load('images/xbb3.png')

        elif event.key == pygame.K_a:
            ship.image = pygame.image.load('images/xbb3.1.png')
        
    if event.key == pygame.K_o:
        pygame.quit()
        sys.exit()

def fire_bullet(ai_settings,screen,ship,bullets,direction):
    if len(bullets)<ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

        if direction == 'up':
            new_bullet.shooting_up = True
            
        elif direction == 'down':
            new_bullet.shooting_down = True
            
        elif direction == 'left':
            new_bullet.shooting_left = True
            
        elif direction == 'right':
            new_bullet.shooting_right = True

        new_bullet.position(ship)    
            
def check_keyup_events(event,ship):
    if event.key == pygame.K_d:
        ship.moving_right = False

    elif event.key == pygame.K_a:
        ship.moving_left = False

    elif event.key == pygame.K_w:
        ship.moving_up = False        

    elif event.key == pygame.K_s:
        ship.moving_down = False

    if ship.healthy:
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            ship.image = pygame.image.load('images/xbb2.png')   

def check_events(ai_settings,screen,ship,bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)

def update_screen(ai_settings,screen,ship,aliens,bullets,bullet2s):      
    screen.fill(ai_settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    for bullet2 in bullet2s.sprites():
        bullet2.draw_bullet()
        
    ship.blitme()
    aliens.draw(screen)
        
    pygame.display.flip()

def update_bullets(ai_settings,screen,ship,aliens,deadaliens,bullets):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0 or bullet.rect.top >= ai_settings.screen_height or bullet.rect.right <= 0 or bullet.rect.left >= ai_settings.screen_width:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings,screen,ship,aliens,deadaliens,bullets)

def update_bullet2s(ai_settings,screen,ship,aliens,deadaliens,bullet2s):
    bullet2s.update()

    for bullet2 in bullet2s.copy():
        if bullet2.rect.top >= ai_settings.screen_height:
            bullet2s.remove(bullet2)

    check_bullet_ship_collisions(ai_settings,screen,ship,aliens,bullet2s)

def update_aliens(aliens):
    check_alien_edges(aliens)
    aliens.update()
        
def create_an_alien(ai_settings,screen,aliens,deadaliens,bullet2s):
    alien = Alien(ai_settings,screen)    
    aliens.add(alien)
    threading.Timer(3,fire_bullet2,(ai_settings,screen,alien,deadaliens,bullet2s)).start()
    
    threading.Timer(2,create_an_alien,(ai_settings,screen,aliens,deadaliens,bullet2s)).start()

def create_an_alien2(ai_settings,screen,aliens,deadaliens):
    alien = Alien(ai_settings,screen)
    alien.alien_kind = 3
    alien.image = pygame.image.load('images/xhh4.png')
    aliens.add(alien)
    
    threading.Timer(3,create_an_alien2,(ai_settings,screen,aliens,deadaliens)).start()

def fire_bullet2(ai_settings,screen,alien,deadaliens,bullet2s):
    if alien not in deadaliens:           
        bullet2 = Bullet2(ai_settings,screen,alien)
        bullet2s.add(bullet2)
        alien.image = pygame.image.load('images/xhh3.png')
        threading.Timer(0.5,recover_alien,(ai_settings,screen,alien)).start()

        threading.Timer(3,fire_bullet2,(ai_settings,screen,alien,deadaliens,bullet2s)).start()
            
def check_bullet_alien_collisions(ai_settings,screen,ship,aliens,deadaliens,bullets):
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,False)

    for alien in aliens:
        if alien not in deadaliens:
            alien.dead_y = alien.y
            
    for alien in collisions.values():
        deadaliens.add(alien)

    for alien in deadaliens:
        alien.healthy = False
        alien.image = pygame.image.load('images/xhh2.png')
        alien.y += ai_settings.alien_speed_factor*((alien.y-alien.dead_y+1)/50)**(1/2)
        if alien.rect.top >= ai_settings.screen_height:
            aliens.remove(alien)
            deadaliens.remove(alien)

def check_bullet_ship_collisions(ai_settings,screen,ship,aliens,bullet2s):
    if ship.healthy:
        if pygame.sprite.spritecollideany(ship,bullet2s):
            ship.image = pygame.image.load('images/xbb3.png')
            ai_settings.ship_speed /= 5
            ship.healthy = False
            threading.Timer(5,recover_ship,(ai_settings,screen,ship)).start()    

def check_alien_edges(aliens):
    for alien in aliens:
        screen_rect = alien.screen.get_rect()
        if alien.rect.right >= screen_rect.right:
            alien.direction *= -1

        elif alien.rect.left <= 0:
            alien.direction *= -1

        elif alien.rect.bottom >= screen_rect.bottom:
            alien.direction_y *= -1

        elif alien.rect.top <= 0:
            alien.direction_y *= -1

def recover_alien(ai_settings,screen,alien):
    alien.image = pygame.image.load('images/xhh1.png')
        
def recover_ship(ai_settings,screen,ship):
    ai_settings.ship_speed *= 5
    ship.image = pygame.image.load('images/xbb2.png')
    ship.healthy = True

    
    
    
