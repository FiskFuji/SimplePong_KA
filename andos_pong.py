#pygame is needed, system import for use of exiting, gfx for better graphics @ ball
import pygame as pg
import sys
from pygame import gfxdraw
import random

#///////////////////////////////////////////////////////////////////////////////
#                               Screen Setup                                   /
#///////////////////////////////////////////////////////////////////////////////

#Initialize pygame
pg.init()

#allows us to change the rate at which everything is calculating/displaying
fps = pg.time.Clock()

#makes your display screen
#(width, height)
screen = pg.display.set_mode((1000, 600))

#make the title`
pg.display.set_caption("Andy's Pong")


#///////////////////////////////////////////////////////////////////////////////
#                                Player 1 (Left)                               /
#///////////////////////////////////////////////////////////////////////////////

class Player: #Making classes will allow changes to be a lot less cumbersome.
    posX = 0 #These variables are set to 0 so that we can call the class later
    posY = 0 #and input values of our own, emphasizes the idea of making changes easier.
    color = (0, 0, 0)
    width = 0
    height = 0
    rec = pg.draw.rect(screen, color, (posX,posY,width,height)) #Actually draws the rectangle.
    rechitbox = pg.Rect((0, 0, 0, 0)) #Makes an invisible rectangle for use of the collide command.

    def __init__(self, x, y, width, height, (r,g,b)): #initializes the class with the variables listed.
        self.posX = x #This function is to make it so that we can "talk" to the class and change values.
        self.posY = y
        self.width = width
        self.height = height
        self.color = (r,g,b)
        self.rechitbox = pg.Rect(self.posX, self.posY, self.width, self.height)

    def updatePlayer(self): #A function to update the rectangle and it's hit box according to it's change in position.
        pg.draw.rect(screen, self.color,(self.posX, self.posY, self.width, self.height))
        self.rechitbox.left = self.posX
        self.rechitbox.top = self.posY

#///////////////////////////////////////////////////////////////////////////////
#                                   Ball                                       /
#///////////////////////////////////////////////////////////////////////////////

class Ball: #A class for the ball will allow us to make changes later to the ball as needed and in an easier manner.
    posX = 0 #All position values passed through the class are the initial position.
    posY = 0
    radius = 0 #This is a dimensional characteristic of the sphere, making it a certain size.
    color = (0, 0, 0)
    dt = 0 #This is the speed of the ball moving around the screen.
    ball = pg.gfxdraw.aacircle(screen, posX, posY, radius, color)
    #This ball is smoother because of the gfx library compared to the normal pg.draw.circle command.
    pg.gfxdraw.filled_circle(screen, posX, posY, radius, color)
    #This makes a separate circle that is filled, but will move along with the initial ball
    #so that it appears as one colored ball.
    ballHitBox = pg.Rect((0, 0, 0, 0))
    #This creates a square hit box around the ball so that we can check for collisions with the rectangles.
    velocity = [0, 0]

    def __init__(self, x, y, radius, (r,g,b), velocity):
        self.posX = x
        self.posY = y
        self.radius = radius
        self.color = (r,g,b)
        self.dt = velocity
        self.ballHitBox = pg.Rect((self.posX, self.posY, self.radius, self.radius))
        self.velocity = [random.randint(-3,-2), 0]

    def moveBall(self):
        self.posX += self.velocity[0]
        self.posY += self.velocity[1]

        
    def updateBall(self): #Like the last two, this will update the ball's image based on it's change in position.
        self.moveBall()
        pg.gfxdraw.aacircle(screen, self.posX, self.posY, self.radius, self.color)
        pg.gfxdraw.filled_circle(screen, self.posX, self.posY, self.radius, self.color)
        self.ballHitBox.left = self.posX
        self.ballHitBox.top = self.posY


#///////////////////////////////////////////////////////////////////////////////
#                         Making everything work                               /
#///////////////////////////////////////////////////////////////////////////////

player1 = Player(30, 225, 15, 150,(255, 255, 255)) #Call the class and give it arguments in the form of the values we want.
player2 = Player(970, 225, 15, 150,(255, 255, 255))
ball = Ball(500, 300, 15, (255, 255, 255), 1)
keys = [] #Store the keys that were pressed


while True: #This will keep everything running forever and in "real-time"
    screen.fill((0, 0, 0))
    fps.tick(60) #Dictates how fast everything is being displayed.
    
    keys = pg.key.get_pressed()
    
    player1.updatePlayer() #Makes sure that the position always changes based on the previous while loops.
    player2.updatePlayer()
    ball.updateBall()
    pg.display.update()

    
    if (keys[pg.K_w] and player1.posY > 0):
        player1.posY -= 10 #If player 1 presses the w key, increment the rectangle by 20 units in the y-position.

    if (keys[pg.K_s] and player1.posY+player1.height < 600):
        player1.posY += 10 #If player 1 presses the s key, decrement the rectangle by 20 units in the y-position.

    if (keys[pg.K_UP] and player2.posY > 0):
        player2.posY -= 10 #If player 2 presses the up arrow key, increment the rectangle by 20 units in the y-position.

    if (keys[pg.K_DOWN] and player2.posY+player1.height < 600):
        player2.posY += 10 #If player 2 pressed the down arrow key, decrement the rectangle by 20 units in the y-position.

    
    if (ball.ballHitBox.colliderect(player1.rechitbox)):
        ball.velocity[0] = -ball.velocity[0]


    for event in pg.event.get(): #Allows us to quit the program.
        if event.type == pg.QUIT:
            pg.quit(); sys.exit();
