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
#               9.12.2016: Started.                                            #
#               10.3.2016: Close to MVP.                                       #
#               10.7.2016: MVP Finished. Features mostly complete. Commenting  #
#                           needed, last 2 features would be to make the whole #
#                           program in a single class and create a simple AI   #
#                           with a start screen menu.                          # 
#                                                                              #
#==============================================================================#

#===Begin Program==============================================================#

#------Begin Imports-----------------------------------------------------------#
import pygame as pg
import sys
import random

#------Initialize Necessary Components-----------------------------------------#
# Initialize a random seed.
random.seed(None)

# Initialize PyGame and a Clock object.
pg.init()
CL = pg.time.Clock()

#:::::::::::::::::::::::#
#_______Versioning______#
verNo = 1.0             #
#:::::::::::::::::::::::#

# Initialize the display and the caption; as well as a system font.
screen = pg.display.set_mode((400, 440))
pg.display.set_caption("Simple Pong v" + str(verNo))
scorefont = pg.font.SysFont("Monospace", 26)

# Is the program running?
RUNNING = True

#===CLASS Definition: Player_==================================================#
# This class represents player objects. The class contains members that alter  # 
# the player's rectangle object, color, width, height, etc.                    # 
#------------------------------------------------------------------------------#
class player:
    
    # Some important data members; declaration of said members.
    initialized = False
    posx = 0
    posy = 0
    width = 0
    height = 0
    RGB = (0, 0, 0)
    hitbox = pg.Rect((0, 0), (0, 0))
    score = 0

    #___:::Initialize:::___
    #   Values passed:
    # Implicit Self, Initial X position in pixels, Initial Y position in
    # pixels, the width of the player in pixels, height of the player in
    # pixels, RGB tuple representing the color of the player.
    def __init__(self, startx, starty, width, height, (r, g, b)):

        # Set the initialized to True.
        self.initialized = True

        # Assign the player attributes.
        self.posx = startx
        self.posy = starty
        self.width = width
        self.height = height
        self.RGB = (r, g, b)

        # Draw the rectangle to the screen and create a Rect object around
        # the drawn rectangle.
        pos = pg.draw.rect(screen, self.RGB, ((startx, starty), (width, height)))
        self.hitbox = pg.Rect((self.posx, self.posy), (self.width, self.height))

    #___:::Update Player:::___
    #   Values passed:
    # Implicit Self.
    def updatePlayer(self):

        # Update the hitbox of the player when called.
        self.hitbox.left = self.posx
        self.hitbox.top = self.posy

        # Draw the rectangle again.
        pos = pg.draw.rect(screen, self.RGB, ((self.posx, self.posy), (self.width, self.height)))
#===END OF CLASS PLAYER========================================================#

    
#===CLASS Definition: Ball_====================================================#
# This class contains information pertaining to the ball. Only one of these    #
# should be created, however, more can be made with slight changes. Members    #
# include size of the ball, initial position, its velocity, and a Rect object. #
#------------------------------------------------------------------------------#
class ball:

    # Declaration of important member data.
    posx = 0
    posy = 0
    width = 0
    height = 0
    RGB = (0, 0, 0)
    velocity = [0, 0]
    sideToGo = 1
    hitbox = pg.Rect((0, 0), (0, 0))
    selftimer = 0

    #___:::Initialize:::___
    #   Values passed:
    # Implicit Self, starting X position in pixels, starting Y position in
    # pixels, width of the ball in pixels, height of the ball in pixels, and
    # RGB tuple representing the color of the ball.
    def __init__(self, startx, starty, width, height, (r, g, b)):

        # Initialize a Clock object for the ball for timed events.
        self.selfclock = pg.time.Clock()

        # Assign member data to passed variables.
        self.posx = startx
        self.posy = starty
        self.width = width
        self.height = height
        self.RGB = (r, g, b)

        # Velocity is a random value, always going to the left first.
        self.velocity = [random.randint(-3, -2), random.randint(-2, 2)]

        # Draw the ball and its Rect object associated with it.
        pos = pg.draw.rect(screen, self.RGB, ((self.posx, self.posy), (self.width, self.height)))
        self.hitbox = pg.Rect((self.posx, self.posy), (self.width, self.height))

    #___:::Move Ball:::___
    #   Values passed:
    # Implicit Self.
    def moveBall(self):

        # Add the current velocity of the ball to its current position.
        self.posx += self.velocity[0]
        self.posy += self.velocity[1]

    #___:::Update the Ball:::___
    #   Values passed:
    # Implicit Self.
    def updateBall(self):

        # Call the moveBall function to actually move it before re-drawing it.
        self.moveBall()

        # Update the hitbox of the ball.
        self.hitbox.left = self.posx
        self.hitbox.top = self.posy
        self.hitbox.width = self.width
        self.hitbox.height = self.height
        
        # Re-draw the ball.
        pos = pg.draw.rect(screen, self.RGB, ((self.posx, self.posy), (self.width, self.height)))

    #___:::Restart the Ball:::___
    #   Values passed:
    # Implicit Self.
    def restartBall(self):

        # Set the ball timer for 4 seconds. (60 frames/sec, 4 seconds)
        self.selftimer = 60 * 4

        # Reset the ball's position.
        self.posx   = 193
        self.posy   = 193
        
        #:::::::::::::::::::::::::::#
        #__Optional: Reset Players__#
        ##p1.posy     = 150         
        ##p2.posy     = 150         
        #:::::::::::::::::::::::::::#

        # Check which player the ball should be going to.
        if(self.sideToGo == 1):
            # The ball velocity should go towards Player 1 (negative).
            self.velocity = [random.randint(-3, -2), random.randint(-2, 2)]

        # Ball should be going to Player 2.
        elif(self.sideToGo == 2):
            #The ball velocity should go towards Player 2 (positive).
            self.velocity = [random.randint(2, 3), random.randint(-2, 2)]

        # When restarting the ball, count down from 3. 
        while(self.selftimer >= 60):
            # Keep the rate at 60 iterations.
            self.selfclock.tick(60)

            # When timer 'equals' 3, draw the board, players and the timer.
            if(self.selftimer / 60 == 3):
                drawBoard()
                p1.updatePlayer()
                p2.updatePlayer()
                screen.blit(scorefont.render("3", 1, (0, 255, 255)), (193, 188))

            # When timer 'equals' 2, draw the board, players and the timer. 
            elif(self.selftimer / 60 == 2):
                drawBoard()
                p1.updatePlayer()
                p2.updatePlayer()
                screen.blit(scorefont.render("2", 1, (0, 255, 255)), (193, 188))

            # When timer 'equals' 1, draw the board, players and the timer.
            elif(self.selftimer / 60 == 1):
                drawBoard()
                p1.updatePlayer()
                p2.updatePlayer()
                screen.blit(scorefont.render("1", 1, (0, 255, 255)), (193, 188))

            # Update the display.
            pg.display.update()

            # Decrease the timer by 1 each iteration.
            self.selftimer -= 1
#===END OF CLASS BALL==========================================================#

#------Definition: Drawing the Board-------------------------------------------#
#___:::Draw the Board:::___
# Draw the board with the rectangles down the middle; as well as the circle.
def drawBoard():
    # Fill the screen with black.
    screen.fill((0, 0, 0))

    # Draw all the rectangles.
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

    # Draw the circle in the center.
    pg.draw.circle(screen, (128, 128, 128), (200, 201), 25, 1)

    # Draw the scores of each player, and the word "SCORE".
    screen.blit(scorefont.render(str(p1.score), 1, (255, 255, 255)), (5, 410))
    screen.blit(scorefont.render(str(p2.score), 1, (255, 255, 255)), (378, 410))
    screen.blit(scorefont.render("SCORE",       1, (255, 255, 255)), (161, 410))

#------'MAIN' Program----------------------------------------------------------#
# Make the player objects and the ball object.
p1      = player(5,   150, 15, 100, (255, 255, 255))
p2      = player(380, 150, 15, 100, (255, 255, 255))
ball    = ball(193, 193, 14, 14, (0, 255, 255))

# Create 4 Rect objects to keep track of the top of the screen, bottom of the
# screen, the player 1's goal, and the player 2's goal.
topOfScreen     = pg.Rect((0, 0),   (400, 1))
bottomOfScreen  = pg.Rect((0, 401), (400, 1))
player1Goal     = pg.Rect((0, 0),   (2, 401))
player2Goal     = pg.Rect((400, 0),   (-2, 401))

# Initialize a list of which keys are being pressed.
keys = []

# Flag to keep track of whether or not the first countdown has been completed.
initialCountdown = True

# Outer Main Loop.
while True:

    # Loop that occurs while the program is 'Running'.
    while RUNNING:

        # Countdown if the initial timer hasn't been done yet.
        if(initialCountdown):
            timer = 60 * 4

            # Timer that counts down from 3.
            while(timer >= 60):
                CL.tick(60)

                # Display a timer showing '3'.
                if(timer / 60 == 3):
                    drawBoard()
                    p1.updatePlayer()
                    p2.updatePlayer()
                    screen.blit(scorefont.render("3", 1, (0, 255, 255)), (193, 188))

                # Display a timer showing '2'.
                elif(timer / 60 == 2):
                    drawBoard()
                    p1.updatePlayer()
                    p2.updatePlayer()
                    screen.blit(scorefont.render("2", 1, (0, 255, 255)), (193, 188))

                # Display a timer showing '1'.
                elif(timer / 60 == 1):
                    drawBoard()
                    p1.updatePlayer()
                    p2.updatePlayer()
                    screen.blit(scorefont.render("1", 1, (0, 255, 255)), (193, 188))

                # Update the display.
                pg.display.update()

                # Decrease the timer.
                timer -= 1

            # Set the internal flag to false.
            initialCountdown = False

        #------After the initial timer:------#
        # 60 Iterations per second.
        CL.tick(60)

        # Draw the board each iteration.
        drawBoard()

        # Update the ball, and players each iteration.
        ball.updateBall()
        p1.updatePlayer()
        p2.updatePlayer()

        # Update the display.
        pg.display.update()

        # Update the list of pressed keys.
        keys = pg.key.get_pressed()
        
        #:::::::::::::::::::::::::::::::::::::::::::::::::::#
        #___________Optional: Draw the Hitboxes.____________#
        ##pg.draw.rect(screen, (255, 0, 0), p1.hitbox, 1)
        ##pg.draw.rect(screen, (255, 0, 0), p2.hitbox, 1)
        ##pg.draw.rect(screen, (255, 0, 0), player1Goal, 1)
        ##pg.draw.rect(screen, (255, 0, 0), player2Goal, 1)
        ##pg.draw.rect(screen, (255, 0, 0), ball.hitbox, 1)
        #:::::::::::::::::::::::::::::::::::::::::::::::::::#

        #:::::::::::::::::::::::::::::::::::::::::::::::::::#
        #_____Optional: Print the Velocity and Position_____#
        ##print ball.velocity
        ##print ball.hitbox.center
        #:::::::::::::::::::::::::::::::::::::::::::::::::::#
        
        #------Large Conditional Branches------#

        #---Player Movements-------------------#
        # Player 1 Presses 'W' key.
        if((keys[pg.K_w]) and (p1.posy >= 1) and (not keys[pg.K_s])):
            p1.posy -= 4

        # Player 1 Presses 'S' key.
        if((keys[pg.K_s]) and (p1.posy+100 <= 399) and (not keys[pg.K_w])):
            p1.posy += 4

        # Player 2 Presses 'UP' arrow.
        if((keys[pg.K_UP]) and (p2.posy >= 1) and (not keys[pg.K_DOWN])):
            p2.posy -= 4

        # Player 2 Presses 'DOWN' arrow.
        if((keys[pg.K_DOWN]) and (p2.posy+100 <= 399) and (not keys[pg.K_w])):
            p2.posy += 4

        #---Ball Collisions--------------------#
        # Ball collides with player 1 and is not past the paddle:
        if( (ball.hitbox.colliderect(p1.hitbox)) and (ball.hitbox.center[0] > 20) ):

            # Make the curent X-Velocity negative.
            ball.velocity[0] = -ball.velocity[0]

            # If the X-Velocity is below 4.3, increase it.
            if(ball.velocity[0] < 4.3):
                ball.velocity[0] += 0.1

            # Random increase of Y-Velocity. 50% to be a negative or positive.
            if(random.randint(1,2) == 1):
                
                # Adds a random value from 0.0 - 1.0.
                ball.velocity[1] += random.random()
                
            else:
                # Subtracts a random value from 0.0 - 1.0.
                ball.velocity[1] -= random.random()

        # Ball collides with player 2 and is not past the paddle.
        if( (ball.hitbox.colliderect(p2.hitbox)) and (ball.hitbox.center[0] < 380) ):

            # Make the current X-Velocity negative.
            ball.velocity[0] = -ball.velocity[0]

            # If the current X-Velocity is above -4.3, decrease it further.
            if(ball.velocity[0] > -4.3):
               ball.velocity[0] -= 0.1

            # Random increase of the Y-Velocity. 50% to be negative/positive.
            if(random.randint(1,2) == 1):

                # Adds a random value from 0.0 - 1.0.
                ball.velocity[1] += random.random()

            else:
                # Subtracts a random value from 0.0 - 1.0.
                ball.velocity[1] -= random.random()

        # Ball collides with the bottom of the screen.
        if( (ball.hitbox.colliderect(bottomOfScreen)) and ((ball.hitbox.center[0] > 20) or (ball.hitbox.center[0] < 380)) ):

            # Make the current Y-Velocity negative.
            ball.velocity[1] = -ball.velocity[1]

            # If the Y-Velocity is greater than -2.6, increase it.
            if(ball.velocity[1] > -2.60):
                ball.velocity[1] -= 0.15

        # Ball collides with the top of the screen.
        if( (ball.hitbox.colliderect(topOfScreen)) and ((ball.hitbox.center[0] > 20) or (ball.hitbox.center[0] < 380)) ):

            # Make the current Y-Velocity negative.
            ball.velocity[1] = -ball.velocity[1]

            # If the Y-Velocity is less than 2.6, increase it.
            if(ball.velocity[1] < 2.60):
                ball.velocity[1] += 0.15

        #---Score Checking---------------------#
        # If the player 1's score is 5, they win.
        if(p1.score == 5):

            # Mini While Loop for the winning screen.
            while RUNNING:

                # Get the mouse position.
                mPos = pg.mouse.get_pos()

                # Fill the screen with black each loop, then draw the
                # necessary words / rectangles.
                screen.fill((0, 0, 0))
                qButton = pg.Rect((150, 300), (100, 40))
                pg.draw.rect(screen, (255, 0, 0), qButton, 2)
                screen.blit(scorefont.render(("Player 1 wins!"), 1, (0, 255, 255)), (100, 188))

                # If the mouse is in the Quit button, light up the word 'Quit'
                if(qButton.collidepoint(mPos) == 1):
                    screen.blit(scorefont.render("Quit", 1, (255, 0, 0)),   (170, 305))
                    screen.blit(scorefont.render("Quit", 1, (255, 0, 255)), (171, 305))

                # Otherwise, draw it regularly.
                else:
                    screen.blit(scorefont.render("Quit", 1, (255, 0, 0)), (170, 305))

                # Update the display.
                pg.display.update()

                # Mini-Event Handler:
                for e in pg.event.get():

                    # Checks for pressing the 'X' button on the window.
                    if e.type == pg.QUIT:
                        pg.quit(); sys.exit()

                    # Checks for the mouse button being pressed inside the
                    # quit button.
                    elif ((e.type == pg.MOUSEBUTTONUP) and (qButton.collidepoint(mPos) == 1)):
                        pg.quit(); sys.exit()

        # If the player 2's score is 5, they win.
        elif(p2.score == 5):

            # Mini While Loop for the winning screen.
            while RUNNING:

                # Get the mouse position.
                mPos = pg.mouse.get_pos()

                # Fill the screen with black and draw the necessary
                # components and rectangles.
                screen.fill((0, 0, 0))
                qButton = pg.Rect((150, 300), (100, 40))
                pg.draw.rect(screen, (255, 0, 0), qButton, 2)
                screen.blit(scorefont.render(("Player 2 wins!"), 1, (0, 255, 255)), (100, 188))

                # If the mouse is inside the Quit button, make it
                # light up.
                if(qButton.collidepoint(mPos) == 1):
                    screen.blit(scorefont.render("Quit", 1, (255, 0, 0)),   (170, 305))
                    screen.blit(scorefont.render("Quit", 1, (255, 0, 255)), (171, 305))

                # Otherwise, draw the Quit text normally.
                else:
                    screen.blit(scorefont.render("Quit", 1, (255, 0, 0)), (170, 305))

                # Update the display.
                pg.display.update()
                
                # Mini-Event Handler.    
                for e in pg.event.get():

                    # Checks for pressing the 'X' button on the window.
                    if e.type == pg.QUIT:
                        pg.quit(); sys.exit()

                    # Checks for the mouse button being pressed inside the
                    # quit button.
                    elif ((e.type == pg.MOUSEBUTTONUP) and (qButton.collidepoint(mPos) == 1)):
                        pg.quit(); sys.exit()

        #---Player Scoring Mechanic------------#
        # If the ball passes the edge of the screen, on Player 2's side:
        # Increase player 1's score and restart the ball.
        if(ball.hitbox.center[0] > 420):

            # Increase player 1's score.
            p1.score += 1

            # If the score does not equal 5, restart the ball and change
            # the side it needs to go to.
            if(p1.score != 5):
                ball.sideToGo = 1
                ball.restartBall()

        # If the ball passes the edge of the screen on Player 1's side:
        # Increase player 2's score and restart the ball.
        if(ball.hitbox.center[0] < -20):

            # Increase player 2's score.
            p2.score += 1

            # If the score does not equal 5, restart the ball and change
            # the side it needs to go to.
            if(p2.score != 5):
                ball.sideToGo = 2
                ball.restartBall()

        #------Event Handler-------------------#
        for e in pg.event.get():

            # Checks if the 'X' button on the window has been pressed.
            if e.type == pg.QUIT:
                pg.quit(); sys.exit()

            # Checks if the 'P' key was pressed to pause the game.
            elif(e.type == pg.KEYDOWN and e.key == pg.K_p):

                    # Set running to false, fill the screen with black and
                    # write the word 'Paused'.
                    RUNNING = False
                    screen.fill((0, 0, 0))
                    screen.blit(scorefont.render("PAUSED", 1, (255, 0, 255)), (155, 195))
                    pg.display.update()

    # If the program is not running, use this while loop:
    while not(RUNNING):

        # Event Handler:
        for e in pg.event.get():

            # Checks for the 'X' button on the window being pressed.
            if e.type == pg.QUIT:
                pg.quit(); sys.exit()

            # If the 'P' key is pressed, un-pause the game.
            elif(e.type == pg.KEYDOWN and e.key == pg.K_p):

                # Set the running flag to True again.
                RUNNING = True

#===End of Program=============================================================#
