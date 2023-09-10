import pygame
import os
import sys
pygame.font.init()
# pygame.mixer.init()

WIDTH,HEIGHT = 900,900
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Game by Prabin")

SPACESHIP_WIDTH,SPACESHIP_HEIGHT =  40,50
COLOR = (255,255,255)
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLET = 5
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
 
HEALTH_FONT = pygame.font.SysFont('comicsans', 20)
WINNER_FONT  = pygame.font.SysFont('comicsans', 50)
TEXT_FONT = pygame.font.SysFont('comicsans', 25)

YELLOW_HIT = pygame.USEREVENT + 1  #number
RED_HIT = pygame.USEREVENT + 2      #number

# BULLET_HIT_SOUND = pygame.mixer.load(os.path.join('Assets','Grenade+1.mp3'))
# BULLET_FIRE_SOUND = pygame.mixer.load(os.path.join('Assets','Gun+Silencer.mp3'))

RECT_BORDER = pygame.Rect(WIDTH//2 - 10, 0, 20, HEIGHT)

YELLOW_SPACESHIP = pygame.image.load(os.path.join('python','Assets','spaceship_yellow.png'))
RED_SPACESHIP = pygame.image.load(os.path.join('python','Assets','spaceship_red.png'))
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('python','Assets','space.png')),(WIDTH, HEIGHT))

RESIZED_YELLOW = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RESIZED_RED = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

class GameState():
    def __init__(self):
        self.state = 'intro'
     
    def main_game(self):
        
        
        red = pygame.Rect(800, 500, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        yellow = pygame.Rect(100, 500, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
        red_bullet =[]
        yellow_bullet =[]
        red_health = 10
        yellow_health = 10
        clock = pygame.time.Clock()
        
        run = True
        while run: 
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z and len(yellow_bullet) < MAX_BULLET:
                        bullet = pygame.Rect(yellow.x + yellow.width,yellow.y + yellow.height//2 - 2, 10, 4)
                        yellow_bullet.append(bullet)
                    # BULLET_FIRE_SOUND.play()
                    
                    if event.key == pygame.K_m and len(red_bullet) < MAX_BULLET:
                        bullet = pygame.Rect(red.x - red.width, red.y + red.height//2 - 2, 10, 4)
                        red_bullet.append(bullet)
                    # BULLET_FIRE_SOUND.play()
                    
                    
                if event.type == RED_HIT:
                    red_health -= 1
                # BULLET_HIT_SOUND.play()
                
                if event.type == YELLOW_HIT:
                    yellow_health -= 1
                # BULLET_HIT_SOUND.play()
                
            winner_text = ""
        
            if red_health <= 0:
                winner_text = "YELLOW WINS"
            
            if yellow_health <= 0:
                winner_text = "RED WINS"
            
            if winner_text != "":
                draw_winner(winner_text)
                break
        
            keys_pressed = pygame.key.get_pressed()
        
            yellow_handle_movement(keys_pressed, yellow)
            red_handle_movement(keys_pressed, red)

            handle_bullet(red_bullet, yellow_bullet, red, yellow)
        
            draw_window(red, yellow, red_bullet, yellow_bullet, red_health, yellow_health)
        
        main()
       
    def intro(self):
        
        # # WIN.blit(SPACE, (0,0))
        # # pygame.display.update()
        # pygame.display.update()
        run = True
        clock = pygame.time.Clock()
        while run:
            
            clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    
                # sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    
                    if event.button == 1 :
                        
                        # draw_winner("Ready to Play")
                        # pygame.time.delay(100)
                        
                        WIN.fill(BLACK)
                        
                        draw_winner('3')
                        pygame.time.delay(100)
                        WIN.fill(BLACK)
                        
                        draw_winner('2')
                        pygame.time.delay(100)
                        WIN.fill(BLACK)
                    
                        draw_winner('1')
                        pygame.time.delay(100)
                        WIN.fill(BLACK)
                        
                        pygame.display.update()
                        
                        self.main_game()
                    
                    if event.button == 3:
                        run = False
    

    def state_manager(self):
        if self.state == 'intro':
            self.intro()
        if self.state == 'main_game':
            self.main_game()
        

def yellow_handle_movement(keys_pressed, yellow):
     
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #up
        yellow.y -= VEL
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL < 440: #right
        yellow.x += VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL < 840: #down
        yellow.y += VEL
    
def red_handle_movement(keys_pressed, red):
    
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #top
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL < 850: #down
        red.y += VEL
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > 440: #left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL < 850: #right
        red.x  += VEL

def handle_bullet(red_bullet, yellow_bullet, red, yellow):
    for bullet in yellow_bullet:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullet.remove(bullet)
        if bullet.x > WIDTH:
            yellow_bullet.remove(bullet)
        elif bullet.x < 0:
            yellow_bullet.remove(bullet)
    
    for bullet in red_bullet:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullet.remove(bullet)
        if bullet.x > WIDTH:
            red_bullet.remove(bullet)
        elif bullet.x < 0:
            red_bullet.remove(bullet)
    
    
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, RECT_BORDER )
    
    redhealth_text = HEALTH_FONT.render("HEALTH : " + str(red_health), 1, WHITE)
    yellowhealth_text = HEALTH_FONT.render("HEALTH : "+str(yellow_health), 1, WHITE)
    
   
    WIN.blit(redhealth_text, (WIDTH - redhealth_text.get_width() - 10,10))
    WIN.blit(yellowhealth_text, (10,10))
    
    WIN.blit(RESIZED_YELLOW,(yellow.x,yellow.y))
    WIN.blit(RESIZED_RED, (red.x,red.y))
    
    
    for bullets in red_bullets:
        pygame.draw.rect(WIN, RED, bullets)
    
    for bullets in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullets)
        
    pygame.display.update()
    
def draw_winner(text):
    
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text,(WIDTH//2 - 100 ,HEIGHT//2))
    pygame.display.update()
    pygame.time.delay(300)
    
    
def draw_ahead(text):
    draw_text = TEXT_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (0,HEIGHT//2))
    pygame.display.update()
    pygame.time.delay(200)
    
def main():
    game_state = GameState()
    game_state.state_manager()
        
if __name__ == "__main__":
    draw_ahead("Ready to go ? If yes ( left click ) your mouse Else ( right click ) your mouse")
    
    main()