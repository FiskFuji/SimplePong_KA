#==============================================================================#
#                ___     ___     _         ___                                 #
#               ||  \   //  \   ||\   |   //  \                                #
#               ||__|  ||    |  || \  |  ||  __                                #
#               ||     ||    |  ||  \ |  ||   |                                #
#               ||      \\__/   ||   \|   \\__/                                #
#                                                                              #
#------------------------------------------------------------------------------#
#   Title:      Simple Pong                                                    #
#                                                                              #
#   Author:     Kirk Worley & Andy Kor                                         #
#                                                                              #
#   Abstract:   To create a PyGame (1.9.1) based simple game involving         #
#                   basic physics, similar to the game Pong. Features will     #
#                   include:                                                   #
#                   - VS. a simple AI.                                         #
#                   - VS. a second player.                                     #
#                                                                              #
#   Dates:      ---                                                            #
#               Started: 9.12.2016                                             #
#               -                                                              #
#               -                                                              #
#                                                                              #
#==============================================================================#

#===Begin Program==============================================================#

#------Begin Imports-----------------------------------------------------------#
import pygame as pg
import sys
import random

random.seed(None)
pg.init()
CL = pg.time.Clock()
screen = pg.display.set_mode((400, 440))
scorefont = pg.font.SysFont("Monospace", 26)

class player:
    posx = 0
    posy = 0
    width = 0
    height = 0
    RGB = (0, 0, 0)
    hitbox = pg.Rect((0, 0), (0, 0))
    score = 0
    
    
    def __init__(self, startx, starty, width, height, (r, g, b)):
        self.posx = startx
        self.posy = starty
        self.width = width
        self.height = height
        self.RGB = (r, g, b)
        pos = pg.draw.rect(screen, self.RGB, ((startx, starty), (width, height)))
        self.hitbox = pg.Rect((self.posx, self.posy), (self.width, self.height))
    
    def updatePlayer(self):
        self.hitbox.left = self.posx
        self.hitbox.top = self.posy
        self.hitbox.width = self.width
        self.hitbox.height = self.height
        pos = pg.draw.rect(screen, self.RGB, ((self.posx, self.posy), (self.width, self.height)))
    

class ball:
    posx = 0
    posy = 0
    width = 0
    height = 0
    RGB = (0, 0, 0)
    velocity = [0, 0]
    sideToGo = 1
    hitbox = pg.Rect((0, 0), (0, 0))
    
    def __init__(self, startx, starty, width, height, (r, g, b)):
        self.posx = startx
        self.posy = starty
        self.width = width
        self.height = height
        self.RGB = (r, g, b)
        self.velocity = [random.randint(-3, -2), random.random()]
        pos = pg.draw.rect(screen, self.RGB, ((self.posx, self.posy), (self.width, self.height)))
        self.hitbox = pg.Rect((self.posx, self.posy), (self.width, self.height))

    def moveBall(self):
        self.posx += self.velocity[0]
        self.posy += self.velocity[1]
        
    def updateBall(self):
        self.moveBall()
        pos = pg.draw.rect(screen, self.RGB, ((self.posx, self.posy), (self.width, self.height)))
        self.hitbox.left = self.posx
        self.hitbox.top = self.posy
        self.hitbox.width = self.width
        self.hitbox.height = self.height
        


def drawBoard():
    screen.fill((0, 0, 0))
    
    pg.draw.rect(screen, (128, 128, 128), ((198, 5),   (4, 12)))
    pg.draw.rect(screen, (128, 128, 128), ((198, 25),  (4, 12)))
    pg.draw.rect(screen, (128, 128, 128), ((198, 45),  (4, 12)))
    pg.draw.rect(screen, (128, 128, 128), ((198, 65),  (4, 12)))
    pg.draw.rect(screen, (128, 128, 128), ((198, 85),  (4, 12)))
    pg.draw.rect(screen, (128, 128, 128), ((198, 105), (4, 12)))
    pg.draw.rect(screen, (128, 128, 128), ((198, 125), (4, 12)))
    pg.draw.rect(screen, (128, 128, 128), ((198, 145), (4, 12)))
    pg.draw.rect(screen, (128, 128, 128), ((198, 165), (4, 12)))
    pg.draw.rect(screen, (128, 128, 128), ((198, 185), (4, 12)))
    pg.draw.rect(screen, (128, 128, 128), ((198, 205), (4, 12)))
    pg.draw.rect(screen, (128, 128, 128), ((198, 225), (4, 12)))
    pg.draw.rect(screen, (128, 128, 128), ((198, 245), (4, 12)))
    pg.draw.rect(screen, (128, 128, 128), ((198, 265), (4, 12)))
    pg.draw.rect(screen, (128, 128, 128), ((198, 285), (4, 12)))
    pg.draw.rect(screen, (128, 128, 128), ((198, 305), (4, 12)))
    pg.draw.rect(screen, (128, 128, 128), ((198, 325), (4, 12)))
    pg.draw.rect(screen, (128, 128, 128), ((198, 345), (4, 12)))
    pg.draw.rect(screen, (128, 128, 128), ((198, 365), (4, 12)))
    pg.draw.rect(screen, (128, 128, 128), ((198, 385), (4, 12)))
    pg.draw.rect(screen, (0,   255, 255), ((0,   401), (400, 2)))
    
    screen.blit(scorefont.render(str(p1.score), 1, (255, 255, 255)), (5, 410))
    screen.blit(scorefont.render(str(p2.score), 1, (255, 255, 255)), (378, 410))
    screen.blit(scorefont.render("SCORE",       1, (255, 255, 255)), (161, 410))

    pg.draw.circle(screen, (128, 128, 128), (200, 201), 25, 1)
    

p1      = player(5,   150, 15, 100, (255, 255, 255))
p2      = player(380, 150, 15, 100, (255, 255, 255))
ball    = ball(193, 193, 14, 14, (0, 255, 255))

topOfScreen     = pg.Rect((0, 0),   (400, 1))
bottomOfScreen  = pg.Rect((0, 401), (400, 1))
player1Goal     = pg.Rect((0, 0),   (17, 401))
player2Goal     = pg.Rect((400, 0),   (-17, 401))

keys = []

while True:

    CL.tick(60)
    drawBoard()
    ball.updateBall()
    p1.updatePlayer()
    p2.updatePlayer()
    
    print ball.velocity
    
    pg.draw.rect(screen, (255, 0, 0), player1Goal, 1)
    pg.draw.rect(screen, (255, 0, 0), player2Goal, 1)
    pg.display.update()
    keys = pg.key.get_pressed()

    if((keys[pg.K_w]) and (p1.posy >= 1) and (not keys[pg.K_s])):
            p1.posy -= 3

    if((keys[pg.K_s]) and (p1.posy+100 <= 399) and (not keys[pg.K_w])):
        p1.posy += 3

    if((keys[pg.K_UP]) and (p2.posy >= 1) and (not keys[pg.K_DOWN])):
        p2.posy -= 3

    if((keys[pg.K_DOWN]) and (p2.posy+100 <= 399) and (not keys[pg.K_w])):
        p2.posy += 3

    if( (ball.hitbox.colliderect(p1.hitbox)) and (not ball.hitbox.colliderect(player1Goal)) ):
        ball.velocity[0] = -ball.velocity[0]
        if(not ball.velocity[0] > 3.2):
            ball.velocity[0] += 0.1
            if((ball.velocity[1] > 0) and (not ball.velocity[1] < 1.7)):
               ball.velocity[1] += 0.05

    if( (ball.hitbox.colliderect(p2.hitbox)) and (not ball.hitbox.colliderect(player2Goal)) ):
       ball.velocity[0] = -ball.velocity[0]
       if(not ball.velocity[0] < -3.2):
           ball.velocity[0] -= 0.1

    if( (ball.hitbox.colliderect(bottomOfScreen)) and (not ball.hitbox.colliderect(player1Goal)) ):
        ball.velocity[1] = -ball.velocity[1]
        if(not ball.velocity[1] < -1.7):
            ball.velocity[1] -= 0.1
        
    if( (ball.hitbox.colliderect(topOfScreen)) and (not ball.hitbox.colliderect(player1Goal)) ):
       ball.velocity[1] = -ball.velocity[1]
       if(not ball.velocity[1] > 1.7):
           ball.velocity[1] += 0.1
    
    for e in pg.event.get():

        if e.type == pg.QUIT:
            pg.quit(); sys.exit()


    

