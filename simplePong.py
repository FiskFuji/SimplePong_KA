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
        pos = pg.draw.rect(screen, self.RGB, ((self.posx, self.posy), (self.width, self.height)))
        self.hitbox.left = self.posx
        self.hitbox.top = self.posy

class ball:
    posx = 0
    posy = 0
    width = 0
    height = 0
    RGB = (0, 0, 0)
    velocity = [0, 0]
    hitbox = pg.Rect((0, 0), (0, 0))
    
    def __init__(self, startx, starty, width, height, (r, g, b)):
        self.posx = startx
        self.posy = starty
        self.width = width
        self.height = height
        self.RGB = (r, g, b)
        self.velocity = [0, 0]
        pos = pg.draw.rect(screen, self.RGB, ((self.posx, self.posy), (self.width, self.height)))
        self.hitbox = pg.Rect((self.posx, self.posy), (self.width, self.height))

def drawBoard():
    screen.fill((0, 0, 0))
    pg.draw.rect(screen, (128, 128, 128), ((198, 5), (4, 12)))
    pg.draw.rect(screen, (128, 128, 128), ((198, 25), (4, 12)))
    pg.draw.rect(screen, (128, 128, 128), ((198, 45), (4, 12)))
    pg.draw.rect(screen, (128, 128, 128), ((198, 65), (4, 12)))
    pg.draw.rect(screen, (128, 128, 128), ((198, 85), (4, 12)))
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
    pg.draw.rect(screen, (0, 255, 255),   ((0, 401),  (400, 2)))
    screen.blit(scorefont.render(str(p1.score), 1, (255, 255, 255)), (5, 410))
    screen.blit(scorefont.render(str(p2.score), 1, (255, 255, 255)), (378, 410))
    screen.blit(scorefont.render("SCORE", 1, (255, 255, 255)), (161, 410))
    

p1 = player(5, 5, 15, 100, (255, 255, 255))
p2 = player(380, 5, 15, 100, (255, 255, 255))
pg.key.set_repeat(1, 1)
keys = []

while True:

    CL.tick(60)
    drawBoard()
    p1.updatePlayer()
    p2.updatePlayer()
    pg.display.update()
    mpos = pg.mouse.get_pos()
    keys = pg.key.get_pressed()

    if((keys[pg.K_UP]) and (p1.posy >= 1) and (not keys[pg.K_DOWN])):
            p1.posy -= 3

    if((keys[pg.K_DOWN]) and (p1.posy+100 <= 399) and (not keys[pg.K_UP])):
        p1.posy += 3

    if((keys[pg.K_w]) and (p2.posy >= 1) and (not keys[pg.K_s])):
        p2.posy -= 3

    if((keys[pg.K_s]) and (p2.posy+100 <= 399) and (not keys[pg.K_w])):
        p2.posy += 3
    
    for e in pg.event.get():

        if e.type == pg.QUIT:
            pg.quit(); sys.exit()

        elif e.type == pg.MOUSEBUTTONDOWN and (p1.hitbox.collidepoint(mpos) == 1):
            print "Inside rectangle!"


                

            

            
