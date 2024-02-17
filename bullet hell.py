import pygame
import math
import pygame.gfxdraw
import random
from sys import exit

#starts pygame
pygame.init()

#creating window/display surface ((width, height))
screen = pygame.display.set_mode((800, 400))

#give game a title
pygame.display.set_caption("Bullet hell")
#can chnage icon if you want

#creating clock for fps
clock = pygame.time.Clock()


#regular surface = single image(import, text, colour) needs to be put on display surface to be seen
player = pygame.Surface((20, 20))
player.fill("red")

#making a hitbox(rectangle) for the player
player_rect = player.get_rect(midbottom = (400, 200)).scale_by(0.5)

#making bullets
p = 0
class bullet:
    def __init__(self):
        global p
        self.surface1 = pygame.image.load('bullet image.png')
        self.surface = pygame.transform.scale_by(self.surface1, 0.1)
        #self.surface.fill("white")
        self.angle = random.randint(-60, 60)
        self.surface = pygame.transform.rotate(self.surface, self.angle)
        if p % 2 == 0:
            self.direction = -5
        else:
            self.direction = 5
        if self.direction == 5:
            self.rect = self.surface.get_rect(midbottom =(random.randint(0, 800),random.randint(400, 600))).scale_by(0.75)
        else:
            self.surface = pygame.transform.rotate(self.surface, 180)
            self.rect = self.surface.get_rect(midbottom =(random.randint(0, 800),random.randint(-200, 0))).scale_by(0.75)
        p += 1
        
    def move(self):
        if self.direction == 5:
            self.rect.bottom -= 5 * math.sin(math.radians(90 - abs(self.angle)))
            if self.angle <= 0:
                self.rect.left += 10 * math.cos(math.radians(90 - abs(self.angle)))
            else:
                self.rect.left -= 10 * math.cos(math.radians(90 - abs(self.angle)))

            if self.rect.bottom <= -50:
                self.rect.bottom = random.randint(400, 600)
                self.rect.left = random.randint(0, 800)
        else:
            self.rect.bottom += 5 * math.sin(math.radians(90 - abs(self.angle)))
            if self.angle <= 0:
                self.rect.left -= 10 * math.cos(math.radians(90 - abs(self.angle)))
            else:
                self.rect.left += 10 * math.cos(math.radians(90 - abs(self.angle)))
            if self.rect.bottom >= 450:
                self.rect.bottom = random.randint(-200, 0)
                self.rect.left = random.randint(0, 800)
        screen.blit(self.surface, self.rect)

    def check(self):
        if self.rect.colliderect(player_rect):
            for i in range(50):
                print("Your score was", len(bullets))
            pygame.quit()

bullets = []
bullets.append(bullet())
frames = 0
xmomentum = 0
ymomentum = 0

#keeps code going
#game loop
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
        #player_rect.bottom -= 10
        ymomentum -= 0.3
    if keys[pygame.K_s]:
        #player_rect.bottom += 10
        ymomentum += 0.3
    if keys[pygame.K_a]:
        #player_rect.left -= 10
        xmomentum -= 0.3
    if keys[pygame.K_d]:
        #player_rect.left += 10
        xmomentum += 0.3
        
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
        
    if player_rect.bottom >= 395:
        ymomentum = -3
    if player_rect.bottom <= 5:
        ymomentum = 3
    if player_rect.right >= 795:
        xmomentum = -3
    if player_rect.left <= 5:
        xmomentum = +3
    
    #draw all elements
    #update evrything
    pygame.display.update()
    #if loop is per frame then the speed of the game is based on fps which can vary
    frames += 1
    clock.tick(60)
