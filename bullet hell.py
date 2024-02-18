import pygame
import pygame.font
import math
import pygame.gfxdraw
import random
from sys import exit

mode = "classic"

#starts pygame
pygame.init()

#creating window/display surface ((width, height))
screen = pygame.display.set_mode((800, 600))

#give game a title
pygame.display.set_caption("Bullet hell")
#can chnage icon if you want

#creating clock for fps
clock = pygame.time.Clock()


#regular surface = single image(import, text, colour) needs to be put on display surface to be seen
player = pygame.Surface((20, 20))
player.fill("red")

#making a hitbox(rectangle) for the player
player_rect = player.get_rect(midbottom = (400, 300)).scale_by(0.5)

#making bullets
p = 0
class bullet:
    def __init__(self):
        global p, mode
        self.surface1 = pygame.image.load('bullet image.png')
        self.surface = pygame.transform.scale_by(self.surface1, 0.1)
        #self.surface.fill("white")
        self.angle = random.randint(-60, 60)
        if p % 2 == 0:
            self.direction = -5
        else:
            self.direction = 5

        self.surface = pygame.transform.rotate(self.surface, self.angle)
        global mode
        if mode != "bounce":
            if self.direction == 5:
                self.rect = self.surface.get_rect(midbottom =(random.randint(0, 800),random.randint(600,800))).scale_by(0.75)
            else:
                self.surface = pygame.transform.rotate(self.surface, 180)
                self.rect = self.surface.get_rect(midbottom =(random.randint(0, 800), random.randint(-200, 0))).scale_by(0.75)
        else:
            if self.direction == 5:
                self.rect = self.surface.get_rect(midbottom =(random.randint(0, 800),600)).scale_by(0.75)
            else:
                self.surface = pygame.transform.rotate(self.surface, 180)
                self.rect = self.surface.get_rect(midbottom =(random.randint(0, 800), 40)).scale_by(0.75)
        p += 1
        
    def move(self):
        global mode
        if self.direction == 5:
            self.rect.bottom -= 5 * math.sin(math.radians(90 - abs(self.angle)))
            if self.angle <= 0:
                self.rect.left += 10 * math.cos(math.radians(90 - abs(self.angle)))
            else:
                self.rect.left -= 10 * math.cos(math.radians(90 - abs(self.angle)))
                
            if mode != "bounce":
                if self.rect.bottom <= -50:
                    self.rect.bottom = random.randint(600, 800)
                    self.rect.left = random.randint(0, 800)
        else:
            self.rect.bottom += 5 * math.sin(math.radians(90 - abs(self.angle)))
            if self.angle <= 0:
                self.rect.left -= 10 * math.cos(math.radians(90 - abs(self.angle)))
            else:
                self.rect.left += 10 * math.cos(math.radians(90 - abs(self.angle)))

            if mode != "bounce":    
                if self.rect.bottom >= 650:
                    self.rect.bottom = random.randint(-200, 0)
                    self.rect.left = random.randint(0, 800)
        screen.blit(self.surface, self.rect)

    def check(self):
        global dodge, bullets, last_score, high_score, mode
        if mode == "dodge": 
            if self.rect.colliderect(player_rect) and dodge == 0:
                last_score = len(bullets)
                if last_score > high_score:
                    high_score = last_score
                for i in range(len(bullets) - 1):
                    bullets.pop()
                main_menu()
        else:
            if self.rect.colliderect(player_rect):
                last_score = len(bullets)
                if last_score > high_score:
                    high_score = last_score
                for i in range(len(bullets) - 1):
                    bullets.pop()
                main_menu()

    def bounce(self):
        if self.rect.left <= 0 or self.rect.right >= 800:
            self.angle = 360 - self.angle
            #self.surface = pygame.transform.rotate(self.surface, 180 + 2 * self.angle)
        if self.rect.bottom >= 600:
            if self.direction == 5:
                self.angle = 180 - abs(self.angle)
            else:
                self.angle = 180 - abs(self.angle)
                
        if self.rect.top <= 0:
            if self.direction == 5:
                self.angle = 180 - abs(self.angle)
            else:
                self.angle = 180 - abs(self.angle)
             
            
        

class Button():
    def __init__(self, pos, text_input, font, color):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.color = color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.color)
        self.image = self.text
        self.rect = self.image.get_rect(topleft = (self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(topleft = (self.x_pos, self.y_pos))

    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
        

bullets = []
bullets.append(bullet())
frames = 0
xmomentum = 0
ymomentum = 0
d_frame = -300

def dodger():
    global d_frame, dodge
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN] and frames > d_frame + 300:
        dodge = 1
        d_frame = frames
        player.fill("green")
    if frames > d_frame + 120:
        dodge = 0
        player.fill("red")
def sett():
    global bullets, frames, xmomentum, ymomentum, d_frame, mode
    player_rect.midbottom = (400, 300)
    bullets = []
    frames = 0
    xmomentum = 0
    ymomentum = 0
    d_frame = -300

#keeps code going
#game loop
def play():
    sett()
    pygame.display.set_caption("Play")
    global bullets, frames, xmomentum, ymomentum, d_frame, mode
    while True:
        screen.fill("black")
        #need to check if player closes the game otherwise it would run forever
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        #shows surface on display surface(surface, position)
        #origin for pygame is in top left (right = + x, down = + y)
        #topleft corner of surface is where the coordinate is
        screen.blit(player, player_rect)

        if frames < 300000:
            if frames % 60 == 0:
                bullets.append(bullet())

            for i in range(len(bullets)):
                bullets[i].move()
                bullets[i].check()
                    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            ymomentum -= 0.3
        if keys[pygame.K_s]:
            ymomentum += 0.3
        if keys[pygame.K_a]:
            xmomentum -= 0.3
        if keys[pygame.K_d]:
            xmomentum += 0.3

        if mode == "dodge":
            dodger()
        if mode == "bounce":
            for i in range(len(bullets)):
                bullets[i].bounce()
        
        player_rect.bottom += ymomentum
        player_rect.left += xmomentum
    
        if xmomentum > 0:
            xmomentum -= 0.1
        else:
            xmomentum += 0.1
        if ymomentum > 0:
            ymomentum -= 0.1
        else:
            ymomentum += 0.1
        
        if player_rect.bottom >= 595:
            ymomentum = -3
        if player_rect.bottom <= 5:
            ymomentum = 3
        if player_rect.right >= 795:
            xmomentum = -3
        if player_rect.left <= 5:
            xmomentum = 3

        #if keys[pygame.K_RSHIFT]:
        #    if xmomentum > 0:
        #        xmomentum = 10
        #    else:
        #        xmomentum = -10
        #    if ymomentum > 0:
        #        ymomentum = 10
        #    else:
        #        ymomentum = -10
    
        #draw all elements
        #update evrything
        pygame.display.update()
        #if loop is per frame then the speed of the game is based on fps which can vary
        frames += 1
        clock.tick(60)


def options():
    pygame.display.set_caption("Game modes")
    global mode
    while True:
        screen.fill("black")

        options_mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if classic_button.check_input(options_mouse_pos):
                    mode = "classic"
                    main_menu()
                if dodge_button.check_input(options_mouse_pos):
                    mode = "dodge"
                    main_menu()
                if bounce_button.check_input(options_mouse_pos):
                    mode = "bounce"
                    main_menu()
                
        font = pygame.font.Font('freesansbold.ttf', 48)
        score_font = pygame.font.Font('freesansbold.ttf', 24)
        menu_font = pygame.font.Font('freesansbold.ttf', 64)
        menu_text = menu_font.render("Game Modes:", True, "#b68f40")
        menu_rect = menu_text.get_rect(topleft = (200, 50))

        screen.blit(menu_text, menu_rect)

        classic_button = Button(pos = (100, 150), text_input = "Classic", font = font, color = ("#d7fcd4"))
        dodge_button = Button(pos = (500, 150), text_input = "Dodge", font = font, color = ("#d7fcd4"))
        bounce_button = Button(pos = (100, 300), text_input = "Bounce", font = font, color = ("#d7fcd4"))

        for button in [classic_button, dodge_button, bounce_button]:
            button.update(screen)
            
        pygame.display.update()

last_score = 0
high_score = 0

def main_menu():
    global last_score
    pygame.display.set_caption("Menu")
    while True:
        screen.fill("black")
        
        menu_mouse_pos = pygame.mouse.get_pos()

        font = pygame.font.Font('freesansbold.ttf', 48)
        score_font = pygame.font.Font('freesansbold.ttf', 24)
        menu_font = pygame.font.Font('freesansbold.ttf', 64)
        menu_text = menu_font.render("Main Menu", True, "#b68f40")
        menu_rect = menu_text.get_rect(topleft = (200, 50))

        high_score_button = Button(pos = (400, 220), text_input = "Your high score is " + str(high_score), font = score_font, color = ("#d7fcd4"))
        score_button = Button(pos = (130, 220), text_input = "Your last score was " + str(last_score), font = score_font, color = ("#d7fcd4"))
        play_button = Button(pos = (300, 150), text_input = "Play", font = font, color = ("#d7fcd4"))
        options_button = Button(pos = (220, 300), text_input = "Game modes", font = font, color = ("#d7fcd4"))
        quit_button = Button(pos = (300, 450), text_input = "Quit", font = font, color = ("#d7fcd4"))

        screen.blit(menu_text, menu_rect)

        for button in [play_button, options_button, quit_button, score_button, high_score_button]:
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_input(menu_mouse_pos):
                    play()
                if options_button.check_input(menu_mouse_pos):
                    options()
                if quit_button.check_input(menu_mouse_pos):
                    pygame.quit()
                    exit()

        pygame.display.update()

main_menu()
