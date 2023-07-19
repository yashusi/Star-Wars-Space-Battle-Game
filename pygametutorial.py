import pygame
import os

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))   # WIN is window
pygame.display.set_caption("First Game")

FPS = 60 #frames per second we want out window to refresh. Otherwise, window refreshes as many times as possible depending on machine capibilites
VEL = 5 #rate of movement for our objects/surfaces
BULLET_VEL = 7
MAX_BULLETS = 5
SURFACE_WIDTH, SURFACE_HEIGHT = 120, 80

VD_HIT = pygame.USEREVENT + 1
VN_HIT = pygame.USEREVENT + 2

BORDER = pygame.Rect((WIDTH//2) - 5, 0, 10, HEIGHT)

VDROID_IMAGE = pygame.image.load(os.path.join('vdroid.png'))
VDROID =pygame.transform.scale(VDROID_IMAGE, (SURFACE_WIDTH, SURFACE_HEIGHT))
VENATOR_IMAGE = pygame.image.load(os.path.join('venator.png'))
VENATOR =pygame.transform.flip(pygame.transform.scale(VENATOR_IMAGE, (SURFACE_WIDTH, SURFACE_HEIGHT)), True, False)
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Naboo.webp')), (WIDTH, HEIGHT))

def vdroid_handle_movement(keys, vd):
    if keys[pygame.K_a] and vd.x > 0: #Vulture Droid LEFT
        vd.x -= VEL
    if keys[pygame.K_d] and vd.x < BORDER.x - SURFACE_WIDTH : #Vulture Droid RIGHT
        vd.x += VEL
    if keys[pygame.K_s] and vd.y < HEIGHT - SURFACE_HEIGHT : #Vulture Droid DOWN
        vd.y += VEL
    if keys[pygame.K_w] and vd.y > 0: #Vulture Droid UP
        vd.y -= VEL

def venator_handle_movement(keys, vn):
    if keys[pygame.K_LEFT] and vn.x > BORDER.x: #Venator LEFT
        vn.x -= VEL
    if keys[pygame.K_RIGHT] and vn.x < WIDTH - SURFACE_WIDTH: #Venator RIGHT
        vn.x += VEL
    if keys[pygame.K_DOWN] and vn.y < HEIGHT - SURFACE_HEIGHT: #Venator DOWN
        vn.y += VEL
    if keys[pygame.K_UP] and vn.y > 0: #Venator UP
        vn.y -= VEL

def draw_window(vd, vn, vd_bullets, vn_bullets):
    WIN.blit(BACKGROUND, (0,0))
    pygame.draw.rect(WIN, (255, 255, 255), BORDER)
    WIN.blit(VDROID, (vd.x, vd.y))
    WIN.blit(VENATOR, (vn.x, vn.y))

    for bullet in vd_bullets:
        pygame.draw.rect(WIN, (255,0,0), bullet)
    for bullet in vn_bullets:
        pygame.draw.rect(WIN, (0,0,220), bullet)
    pygame.display.update()

def handle_bullets(vd_bullets, vn_bullets, vd, vn):
    for bullet in vd_bullets:
        bullet.x += BULLET_VEL
        if vn.colliderect(bullet):
            pygame.event.post(pygame.event.Event(VN_HIT))
            vd_bullets.remove(bullet)
        elif bullet.x >= WIDTH:
            vd_bullets.remove(bullet)
    for bullet in vn_bullets:
        bullet.x -= BULLET_VEL
        if vd.colliderect(bullet):
            pygame.event.post(pygame.event.Event(VD_HIT))
            vn_bullets.remove(bullet)
        elif bullet.x <= 0:
            vn_bullets.remove(bullet)

            
#code the handles main loop and functions
def main():
    vd = pygame.Rect(100, 300, SURFACE_WIDTH, SURFACE_HEIGHT)
    vn = pygame.Rect(700, 300, SURFACE_WIDTH, SURFACE_HEIGHT)

    vd_bullets = []
    vn_bullets = []

    key_pressed = False
    clock = pygame.time.Clock()
    run = True
    while(run): #while loop that makes sure game doesn't immedietly opens and closes
        clock.tick(FPS)
        print(key_pressed)
        for event in pygame.event.get():  #gets list of all events and iterates through each event
            if event.type == pygame.QUIT:
                run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL and len(vd_bullets) <= MAX_BULLETS and not key_pressed:
                key_pressed = True
                bullet = pygame.Rect(vd.x + vd.width, vd.y + vd.height//2 - 2, 10, 5)
                vd_bullets.append(bullet)
                print(vd_bullets)
            if event.key == pygame.K_RCTRL and len(vn_bullets) <= MAX_BULLETS and not key_pressed:
                key_pressed = True
                bullet = pygame.Rect(vn.x, vn.y + vn.height//2 - 2, 10, 5)
                vn_bullets.append(bullet)
        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_LCTRL:
                key_pressed = False
            if event.key == pygame.K_RCTRL:
                key_pressed = False
            

        keys_pressed = pygame.key.get_pressed()
        vdroid_handle_movement(keys_pressed, vd)
        venator_handle_movement(keys_pressed, vn)
        handle_bullets(vd_bullets, vn_bullets, vd, vn)
        draw_window(vd, vn, vd_bullets, vn_bullets)
        





    pygame.quit()

if __name__ == "__main__":
    main()