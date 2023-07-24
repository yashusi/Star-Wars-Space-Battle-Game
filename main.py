import pygame
import os
import sys
import random
pygame.font.init()
pygame.init()

#vd is for Vulture Driod and vn is for Venator Class Cruiser

#game window parameters
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))   # WIN is window
pygame.display.set_caption("First Game")

FPS = 60 #frames per second we want out window to refresh. Otherwise, window refreshes as many times as possible depending on machine capibilites

#constants related to game mechanics
VEL = 5                   #rate of movement for our objects/surfaces
BULLET_VEL = 7            #rate of movement for bullets
MAX_BULLETS = 5           #number of bullets that can be shot at once from each side
SURFACE_WIDTH, SURFACE_HEIGHT = 120, 80     #dimensions of the surfaces (vd and vn)
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 30
#creating events in cases that either is hit
VD_HIT = pygame.USEREVENT + 1     
VN_HIT = pygame.USEREVENT + 2

BORDER = pygame.Rect((WIDTH//2) - 5, 0, 10, HEIGHT)   #the middle partition

#constants related to the display and GUI
#bringing in and transforming vd and vn
VDROID_IMAGE = pygame.image.load(os.path.join('vdroid.png'))
VDROID = pygame.transform.scale(VDROID_IMAGE, (SURFACE_WIDTH, SURFACE_HEIGHT))
VENATOR_IMAGE = pygame.image.load(os.path.join('venator.png'))
VENATOR = pygame.transform.flip(pygame.transform.scale(VENATOR_IMAGE, (SURFACE_WIDTH, SURFACE_HEIGHT)), True, False)
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Naboo.webp')), (WIDTH, HEIGHT))
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

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

def draw_window(vd, vn, vd_bullets, vn_bullets, vd_health, vn_health):
    WIN.blit(BACKGROUND, (0,0))
    pygame.draw.rect(WIN, (255, 255, 255), BORDER)  #divider

    vd_health_text = HEALTH_FONT.render("Health:" + str(vd_health), 1, (255,255,255))
    vn_health_text = HEALTH_FONT.render("Health:" + str(vn_health), 1, (255,255,255))
    WIN.blit(vd_health_text, (10, 10))
    WIN.blit(vn_health_text, ((WIDTH - vd_health_text.get_width() - 10), 10))

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

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, (255,255,255))
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
            
def draw_button(text, x, y):
    print("draw")
    button_rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(WIN, (0,140,140), button_rect)
    text_surface = HEALTH_FONT.render(text, True, (255,255,255))
    text_rect = text_surface.get_rect(center=button_rect.center)
    WIN.blit(text_surface, text_rect)
    print("draw 2")
    return button_rect


def main():
    one_p = False
    two_p = False
    WIN.fill((255,255,255))
    one_player_button = draw_button("1 Player", WIDTH // 4, HEIGHT // 2 - BUTTON_HEIGHT // 2)
    two_players_button = draw_button("2 Players", WIDTH // 4 * 3, HEIGHT // 2 - BUTTON_HEIGHT // 2)
    pygame.display.update()
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        #if exit is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Check button clicks
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]

        if one_player_button.collidepoint(mouse_pos) and mouse_clicked:
            print("1 Player selected")
            one_p = True
            break

        elif two_players_button.collidepoint(mouse_pos) and mouse_clicked:
            print("2 Players selected")
            two_p = True
            break
    if one_p:
        print("one player")
        one_player_main()
    elif two_p:
        print("two player")
        two_player_main()
    else:
        print("something went wrong at this place 1")
        


    
#code the handles main loop and functions
def two_player_main():
    vd = pygame.Rect(100, 300, SURFACE_WIDTH, SURFACE_HEIGHT)
    vn = pygame.Rect(700, 300, SURFACE_WIDTH, SURFACE_HEIGHT)

    vd_bullets = []
    vn_bullets = []

    vd_health = 10
    vn_health = 10

    key_pressed = False
    clock = pygame.time.Clock()
    run = True
    while(run): #while loop that makes sure game doesn't immedietly opens and closes
        clock.tick(FPS)
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
            if event.type == VD_HIT:
                vd_health -= 1
            if event.type == VN_HIT:
                vn_health -= 1
        winner_text = ""
        if vd_health <= 0:
            winner_text = "Venator Wins!"

        if vn_health <= 0:
            winner_text = "Vulture Droid Wins!"
        
        if(winner_text != ""):
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        vdroid_handle_movement(keys_pressed, vd)
        venator_handle_movement(keys_pressed, vn)
        handle_bullets(vd_bullets, vn_bullets, vd, vn)
        draw_window(vd, vn, vd_bullets, vn_bullets, vd_health, vn_health)
        
    pygame.quit()


def vdroid_bot_handle_movement(vd_bot, vn):
    
    vd_bot.x += random.randint(-2,2)
    if vd_bot.centery < vn.centery:
        vd_bot.y += VEL
    elif vd_bot.centery > vn.centery:
        vd_bot.y -= VEL


def one_player_main():
    vd_bot = pygame.Rect(100, 300, SURFACE_WIDTH, SURFACE_HEIGHT)
    vn = pygame.Rect(700, 300, SURFACE_WIDTH, SURFACE_HEIGHT)

    vd_bullets = []
    vn_bullets = []

    vd_health = 10
    vn_health = 10

    key_pressed = False
    clock = pygame.time.Clock()
    run = True
    while(run): #while loop that makes sure game doesn't immedietly opens and closes
        clock.tick(FPS)
        for event in pygame.event.get():  #gets list of all events and iterates through each event
            if event.type == pygame.QUIT:
                run = False
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL and len(vn_bullets) <= MAX_BULLETS and not key_pressed:
                    key_pressed = True
                    bullet = pygame.Rect(vn.x, vn.y + vn.height//2 - 2, 10, 5)
                    vn_bullets.append(bullet)
            if event.type == pygame.KEYUP: 
                if event.key == pygame.K_RCTRL:
                    key_pressed = False
            if event.type == VD_HIT:
                vd_health -= 1
            if event.type == VN_HIT:
                vn_health -= 1

        
        winner_text = ""
        if vd_health <= 0:
            winner_text = "Venator Wins!"

        if vn_health <= 0:
            winner_text = "Vulture Droid Wins!"
        
        if(winner_text != ""):
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        vdroid_bot_handle_movement(vd_bot, vn)
        venator_handle_movement(keys_pressed, vn)
        handle_bullets(vd_bullets, vn_bullets, vd_bot, vn)
        draw_window(vd_bot, vn, vd_bullets, vn_bullets, vd_health, vn_health)
        
    pygame.quit()


if __name__ == "__main__":
    main()