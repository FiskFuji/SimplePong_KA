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
#               9.12.2016:  Started.                                           #
#               10.3.2016:  Close to MVP.                                      #
#               10.7.2016:  MVP Finished. Features mostly complete. Commenting #
#                            needed, last 2 features would be to make the      #
#                            whole program in a single class and create a      #
#                            simple AI with a start screen menu.               #
#              10.13.2016:  Finished menu screen addition as well as a very    #
#                            simple prototype AI. As well as an option to make #
#                            the ball change colors randomly when bouncing off #
#                            a surface.                                        # 
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
verNo = 1.1             #
#:::::::::::::::::::::::#

# Initialize the display and the caption; as well as a system font.
screen = pg.display.set_mode((400, 440))
pg.display.set_caption("Simple Pong v" + str(verNo))
scorefont = pg.font.SysFont("Monospace", 26)

# Is the program running?
RUNNING = True

# Constants
__UP__ = 1
__DOWN__ = 2
__P1SIDE__ = 1
__P2SIDE__ = 2
__MOVE__ = 4
__MOVEFAST__ = 5
__STABLE_VELOCITY__ = 4.3
__STABLE_Y_VELOCITY__ = 2.60
__MAX_SCORE__ = 5

# Dictionary that stores game 'data' variables. 
OPS = {
    # Where the screen should 'be'.
    # 0 = Menu
    # 1 = AI or Player
    # 2 = Game 
    "LOCATION": 0,

    # Option of Random Ball.
    # True / False.
    "RANDOMBALL": False,

    # Flag to keep track of whether or not the first countdown has been completed.
    # True / False.
    "INITCOUNTDOWN": True,

    # Internal processor that keeps track of the AI's direction.
    # 1 = UP
    # 2 = DOWN
    "AIDIRECTION": random.randint(__UP__,__DOWN__)
    }

class player:
    """
    #===CLASS Definition: Player_==================================================#
    # This class represents player objects. The class contains members that alter  # 
    # the player's rectangle object, color, width, height, etc.                    # 
    #------------------------------------------------------------------------------#
    """
    
    # Some important data members; declaration of said members.
    initialized = False
    posx = 0
    posy = 0
    width = 0
    height = 0
    RGB = (0, 0, 0)
    hitbox = pg.Rect((0, 0), (0, 0))
    score = 0

    def __init__(self, startx, starty, width, height, (r, g, b)):
        """
        #___:::Initialize:::___
        #   Values passed:
        # Implicit Self, Initial X position in pixels, Initial Y position in
        # pixels, the width of the player in pixels, height of the player in
        # pixels, RGB tuple representing the color of the player.
        """

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

    def updatePlayer(self):
        """
        #___:::Update Player:::___
        #   Values passed:
        # Implicit Self.
        """

        # Update the hitbox of the player when called.
        self.hitbox.left = self.posx
        self.hitbox.top = self.posy

        # Draw the rectangle again.
        pos = pg.draw.rect(screen, self.RGB, ((self.posx, self.posy), (self.width, self.height)))
#===END OF CLASS PLAYER========================================================#

class ball:
    """
    #===CLASS Definition: Ball_====================================================#
    # This class contains information pertaining to the ball. Only one of these    #
    # should be created, however, more can be made with slight changes. Members    #
    # include size of the ball, initial position, its velocity, and a Rect object. #
    #------------------------------------------------------------------------------#
    """

    # Declaration of important member data.
    posx = 0
    posy = 0
    width = 0
    height = 0
    RGB = (0, 0, 0)
    velocity = [0, 0]
    sideToGo = __P1SIDE__
    hitbox = pg.Rect((0, 0), (0, 0))
    selftimer = 0

    def __init__(self, startx, starty, width, height, (r, g, b)):
        """
        #___:::Initialize:::___
        #   Values passed:
        # Implicit Self, starting X position in pixels, starting Y position in
        # pixels, width of the ball in pixels, height of the ball in pixels, and
        # RGB tuple representing the color of the ball.
        """

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

    def moveBall(self):
        """
        #___:::Move Ball:::___
        #   Values passed:
        # Implicit Self.
        """

        # Add the current velocity of the ball to its current position.
        self.posx += self.velocity[0]
        self.posy += self.velocity[1]

    def updateBall(self):
        """
        #___:::Update the Ball:::___
        #   Values passed:
        # Implicit Self.
        """

        # Call the moveBall function to actually move it before re-drawing it.
        self.moveBall()

        # Update the hitbox of the ball.
        self.hitbox.left = self.posx
        self.hitbox.top = self.posy
        self.hitbox.width = self.width
        self.hitbox.height = self.height
        pos = pg.draw.rect(screen, self.RGB, ((self.posx, self.posy), (self.width, self.height)))

    def restartBall(self):
        """
        #___:::Restart the Ball:::___
        #   Values passed:
        # Implicit Self.
        """

        # Set the ball timer for 4 seconds. (60 frames/sec, 4 seconds)
        self.selftimer = 60 * 4
        self.posx   = 193
        self.posy   = 193
        
        #:::::::::::::::::::::::::::#
        #__Optional: Reset Players__#
        ##p1.posy     = 150         
        ##p2.posy     = 150         
        #:::::::::::::::::::::::::::#

        if self.sideToGo == __P1SIDE__:
            self.velocity = [random.randint(-3, -2), random.randint(-2, 2)]

        elif self.sideToGo == __P2SIDE__:
            self.velocity = [random.randint(2, 3), random.randint(-2, 2)]

        # When restarting the ball, count down from 3. 
        while self.selftimer >= 60:
        
            # Keep the rate at 60 iterations.
            self.selfclock.tick(60)

            # When timer 'equals' 3, draw the board, players and the timer.
            if self.selftimer / 60 == 3:
                drawBoard()
                p1.updatePlayer()
                p2.updatePlayer()
                screen.blit(scorefont.render("3", 1, (0, 255, 255)), (193, 188))

            # When timer 'equals' 2, draw the board, players and the timer. 
            elif self.selftimer / 60 == 2:
                drawBoard()
                p1.updatePlayer()
                p2.updatePlayer()
                screen.blit(scorefont.render("2", 1, (0, 255, 255)), (193, 188))

            # When timer 'equals' 1, draw the board, players and the timer.
            elif self.selftimer / 60 == 1:
                drawBoard()
                p1.updatePlayer()
                p2.updatePlayer()
                screen.blit(scorefont.render("1", 1, (0, 255, 255)), (193, 188))

            pg.display.update()
            self.selftimer -= 1
#===END OF CLASS BALL==========================================================#

def drawBoard():
    """
    #___:::Draw the Board:::___
    # Draw the board with the rectangles down the middle; as well as the circle.
    """
    screen.fill((0, 0, 0))

    # Draw all the rectangles.
    screen.lock()
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
    screen.unlock()
    
    pg.draw.circle(screen, (128, 128, 128), (200, 201), 25, 1)
    screen.blit(scorefont.render(str(p1.score), 1, (255, 255, 255)), (5, 410))
    screen.blit(scorefont.render(str(p2.score), 1, (255, 255, 255)), (378, 410))
    screen.blit(scorefont.render("SCORE",       1, (255, 255, 255)), (161, 410))

def randomBallColor(randomRGBOption):
    if randomRGBOption:
        ball.RGB = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    else:
        pass
        
def drawMenu():
    """
    #___:::Draw the Menu:::___
    # Draw all the necessary components of the menu screen. This includes shapes,
    # buttons, etc.
    """
    screen.fill((0, 0, 0))

    # Draw the menu:
    screen.blit(scorefont.render(("Simple Pong v" + str(verNo)), 1, (255, 255, 255)), (78, 150))
    pg.draw.rect(screen, (255, 255, 255), ((130, 190), (140, 45)), 1)
    pg.draw.rect(screen, (255, 255, 255), ((130, 240), (140, 45)), 1)
    screen.blit(scorefont.render("VS. AI", 1, (0, 255, 255)), (155, 200))
    screen.blit(scorefont.render("2 Player", 1, (255, 150, 0)), (136, 250))

    # Draw controls and option box.
    pg.draw.rect(screen, (255, 255, 255), ((80, 304), (20, 20)), 1)
    screen.blit(scorefont.render("Random RGB Ball", 1, (255, 255, 255)), (110, 300))

    # If the random ball option is on, draw an X in the box.
    if OPS["RANDOMBALL"]:
        screen.blit(scorefont.render("X", 1, (255, 255, 255)), (82, 300))

#------'MAIN' Program----------------------------------------------------------#
p1      = player(5,   150, 15, 100, (255, 255, 255))
p2      = player(380, 150, 15, 100, (255, 255, 255))
ball    = ball(193, 193, 14, 14, (0, 255, 255))

# Create 4 Rect objects to keep track of the top of the screen, bottom of the
# screen, the player 1's goal, and the player 2's goal.
topOfScreen     = pg.Rect((0, 0),   (400, 1))
bottomOfScreen  = pg.Rect((0, 401), (400, 1))
player1Goal     = pg.Rect((0, 0),   (2, 401))
player2Goal     = pg.Rect((400, 0),   (-2, 401))

# Create 3 Rect objects to keep track of the menu screen buttons.
VSAI_Button     = pg.Rect((130, 190), (140, 45))
VS2P_Button     = pg.Rect((130, 240), (140, 45))
RANDOMBALL      = pg.Rect((80, 304), (20, 20))

# Initialize a list of which keys are being pressed.
keys = []

#------Menu Screen Loop--------------------------------------------------------#
while OPS["LOCATION"] == 0:
    mPos = pg.mouse.get_pos()
    drawMenu()

    # If the mouse is inside the VS AI button, 'light' it up.
    if VSAI_Button.collidepoint(mPos):
        pg.draw.rect(screen, (255, 255, 255), ((130, 190), (140, 45)), 2)

    # If the mouse is inside the 2Player button, 'light' it up.
    elif VS2P_Button.collidepoint(mPos):
         pg.draw.rect(screen, (255, 255, 255), ((130, 240), (140, 45)), 2)

    # If the mouse is inside the Random RGB option, 'light' it up.
    elif RANDOMBALL.collidepoint(mPos):
         pg.draw.rect(screen, (255, 255, 255), ((80, 304), (20, 20)), 2)

    pg.display.update()

    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit(); sys.exit()

        # Checks if the mouse was clicked in the Rainbow Ball option box.
        elif e.type == pg.MOUSEBUTTONUP and RANDOMBALL.collidepoint(mPos) == 1:
            if OPS["RANDOMBALL"]:
                OPS["RANDOMBALL"] = False
            elif not OPS["RANDOMBALL"]:
                OPS["RANDOMBALL"] = True

        # Checks if the mouse was clicked in the 2-Player box.
        elif e.type == pg.MOUSEBUTTONUP and VS2P_Button.collidepoint(mPos):
            OPS["LOCATION"] = 2

        # Checks if the mouse was clicked in the VS. AI box.
        elif e.type == pg.MOUSEBUTTONUP and VSAI_Button.collidepoint(mPos):
            OPS["LOCATION"] = 1

#------VS. AI Loop-------------------------------------------------------------#
while OPS["LOCATION"] == 1:
    while RUNNING:

        # Countdown if the initial timer hasn't been done yet.
        if OPS["INITCOUNTDOWN"]:
            timer = 60 * 4

            # Timer that counts down from 3.
            while timer >= 60:
                CL.tick(60)

                # Display a timer showing '3'.
                if timer / 60 == 3:
                    drawBoard()
                    p1.updatePlayer()
                    p2.updatePlayer()
                    screen.blit(scorefont.render("3", 1, (0, 255, 255)), (193, 188))

                # Display a timer showing '2'.
                elif timer / 60 == 2:
                    drawBoard()
                    p1.updatePlayer()
                    p2.updatePlayer()
                    screen.blit(scorefont.render("2", 1, (0, 255, 255)), (193, 188))

                # Display a timer showing '1'.
                elif timer / 60 == 1:
                    drawBoard()
                    p1.updatePlayer()
                    p2.updatePlayer()
                    screen.blit(scorefont.render("1", 1, (0, 255, 255)), (193, 188))

                pg.display.update()
                timer -= 1

            OPS["INITCOUNTDOWN"] = False

        #------After the initial timer:------#
        # 60 Iterations per second.
        CL.tick(60)
        drawBoard()
        ball.updateBall()
        p1.updatePlayer()
        p2.updatePlayer()
        pg.display.update()
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
        
        #---Player Movements-------------------#
        # Player 1 Presses 'W' key.
        if keys[pg.K_w] and p1.posy >= 1 and not keys[pg.K_s]:
            p1.posy -= __MOVE__

        # Player 1 Presses 'S' key. +100 is due to length of rectangle.
        if keys[pg.K_s] and p1.posy+100 <= 399 and not keys[pg.K_w]:
            p1.posy += __MOVE__

        #---Make the AI Move-------------------#
        # The AI moves up and down the screen until it hits the edges.
        if p2.posy > 1 and OPS["AIDIRECTION"] == __UP__:
            p2.posy -= __MOVEFAST__

            # If the AI is at the top, reverse direction.
            if p2.posy <= 1:
                OPS["AIDIRECTION"] = __DOWN__

        # The AI moves down until the bottom of the screen. +100 is due to length of rectangle.
        elif p2.posy+100 < 399 and OPS["AIDIRECTION"] == __DOWN__:
            p2.posy += __MOVEFAST__

            # If the AI is at the bottom, reverse direction.
            if p2.posy+100 >= 399:
                OPS["AIDIRECTION"] = __UP__

        #---Ball Collisions--------------------#
        # Ball collides with player 1 and is not past the paddle:
        if ball.hitbox.colliderect(p1.hitbox) and ball.hitbox.center[0] > 20:
            ball.velocity[0] = -ball.velocity[0]

            if ball.velocity[0] < __STABLE_VELOCITY__:
                ball.velocity[0] += 0.1

            # Random increase of Y-Velocity. 50% to be a negative or positive.
            if random.randint(1,2) == 1:                
                ball.velocity[1] += random.random()
            else:
                ball.velocity[1] -= random.random()

            randomBallColor(OPS["RANDOMBALL"])

        # Ball collides with the AI and is not past the paddle.
        if ball.hitbox.colliderect(p2.hitbox) and ball.hitbox.center[0] < 380:
            ball.velocity[0] = -ball.velocity[0]

            # If the current X-Velocity is above -__STABLE_VELOCITY__, decrease it further.
            if ball.velocity[0] > -__STABLE_VELOCITY__:
               ball.velocity[0] -= 0.15

            # Random increase of the Y-Velocity. 50% to be negative/positive.
            if random.randint(1,2) == 1:
                ball.velocity[1] += random.random()
            else:
                ball.velocity[1] -= random.random()

            randomBallColor(OPS["RANDOMBALL"])
            
        # Ball collides with the bottom of the screen.
        if ball.hitbox.colliderect(bottomOfScreen) and (ball.hitbox.center[0] > 20 or ball.hitbox.center[0] < 380):
            ball.velocity[1] = -ball.velocity[1]

            if ball.velocity[1] > -__STABLE_Y_VELOCITY__:
                ball.velocity[1] -= 0.15

            randomBallColor(OPS["RANDOMBALL"])
            
        # Ball collides with the top of the screen.
        if ball.hitbox.colliderect(topOfScreen) and (ball.hitbox.center[0] > 20 or ball.hitbox.center[0] < 380):
            ball.velocity[1] = -ball.velocity[1]

            if ball.velocity[1] < __STABLE_Y_VELOCITY__:
                ball.velocity[1] += 0.15

            randomBallColor(OPS["RANDOMBALL"])
            
        #---Score Checking---------------------#
        if p1.score == __MAX_SCORE__:
            while RUNNING:
                mPos = pg.mouse.get_pos()

                # Draw the necessary words / rectangles.
                screen.fill((0, 0, 0))
                qButton = pg.Rect((150, 300), (100, 40))
                pg.draw.rect(screen, (255, 0, 0), qButton, 2)
                screen.blit(scorefont.render(("Player 1 wins!"), 1, (0, 255, 255)), (100, 188))

                # If the mouse is in the Quit button, light up the word 'Quit'
                if qButton.collidepoint(mPos) == 1:
                    screen.blit(scorefont.render("Quit", 1, (255, 0, 0)),   (170, 305))
                    screen.blit(scorefont.render("Quit", 1, (255, 0, 255)), (171, 305))
                else:
                    screen.blit(scorefont.render("Quit", 1, (255, 0, 0)), (170, 305))

                pg.display.update()

                for e in pg.event.get():
                    if e.type == pg.QUIT:
                        pg.quit(); sys.exit()

                    elif e.type == pg.MOUSEBUTTONUP and qButton.collidepoint(mPos) == 1:
                        pg.quit(); sys.exit()

        elif p2.score == __MAX_SCORE__:
            while RUNNING:
                mPos = pg.mouse.get_pos()

                # Draw the components and rectangles.
                screen.fill((0, 0, 0))
                qButton = pg.Rect((150, 300), (100, 40))
                pg.draw.rect(screen, (255, 0, 0), qButton, 2)
                screen.blit(scorefont.render(("AI Player wins!"), 1, (0, 255, 255)), (90, 188))

                # If the mouse is inside the Quit button, make it
                # light up.
                if qButton.collidepoint(mPos) == 1:
                    screen.blit(scorefont.render("Quit", 1, (255, 0, 0)),   (170, 305))
                    screen.blit(scorefont.render("Quit", 1, (255, 0, 255)), (171, 305))
                else:
                    screen.blit(scorefont.render("Quit", 1, (255, 0, 0)), (170, 305))

                pg.display.update()
                
                for e in pg.event.get():
                    if e.type == pg.QUIT:
                        pg.quit(); sys.exit()

                    elif e.type == pg.MOUSEBUTTONUP and qButton.collidepoint(mPos) == 1:
                        pg.quit(); sys.exit()

        #---Player Scoring Mechanic------------#
        # If the ball passes the edge of the screen, on the AI's side:
        if ball.hitbox.center[0] > 420:
            p1.score += 1

            if p1.score != __MAX_SCORE__:
                ball.sideToGo = __P1SIDE__
                ball.restartBall()

        # If the ball passes the edge of the screen on Player 1's side:
        if ball.hitbox.center[0] < -20:
            p2.score += 1

            if p2.score != __MAX_SCORE__:
                ball.sideToGo = __P2SIDE__
                ball.restartBall()

        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit(); sys.exit()

            # Checks if the 'P' key was pressed to pause the game.
            elif e.type == pg.KEYDOWN and e.key == pg.K_p:
                    RUNNING = False
                    screen.fill((0, 0, 0))
                    screen.blit(scorefont.render("PAUSED", 1, (255, 0, 255)), (155, 195))
                    pg.display.update()

    while not RUNNING:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit(); sys.exit()

            # If the 'P' key is pressed, un-pause the game.
            elif e.type == pg.KEYDOWN and e.key == pg.K_p:
                RUNNING = True            

#------2 Player Loop-----------------------------------------------------------#
while OPS["LOCATION"] == 2:
    while RUNNING:

        # Countdown if the initial timer hasn't been done yet.
        if OPS["INITCOUNTDOWN"]:
            timer = 60 * 4

            # Timer that counts down from 3.
            while timer >= 60:
                CL.tick(60)

                # Display a timer showing '3'.
                if timer / 60 == 3:
                    drawBoard()
                    p1.updatePlayer()
                    p2.updatePlayer()
                    screen.blit(scorefont.render("3", 1, (0, 255, 255)), (193, 188))

                # Display a timer showing '2'.
                elif timer / 60 == 2:
                    drawBoard()
                    p1.updatePlayer()
                    p2.updatePlayer()
                    screen.blit(scorefont.render("2", 1, (0, 255, 255)), (193, 188))

                # Display a timer showing '1'.
                elif timer / 60 == 1:
                    drawBoard()
                    p1.updatePlayer()
                    p2.updatePlayer()
                    screen.blit(scorefont.render("1", 1, (0, 255, 255)), (193, 188))

                pg.display.update()
                timer -= 1

            # Set the internal flag to false.
            OPS["INITCOUNTDOWN"] = False

        #------After the initial timer:------#
        CL.tick(60)
        drawBoard()
        ball.updateBall()
        p1.updatePlayer()
        p2.updatePlayer()
        pg.display.update()
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
        
        #---Player Movements-------------------#
        # Player 1 Presses 'W' key.
        if keys[pg.K_w] and p1.posy >= 1 and not keys[pg.K_s]:
            p1.posy -= __MOVE__

        # Player 1 Presses 'S' key.
        if keys[pg.K_s] and p1.posy+100 <= 399 and not keys[pg.K_w]:
            p1.posy += __MOVE__

        # Player 2 Presses 'UP' arrow.
        if keys[pg.K_UP] and p2.posy >= 1 and not keys[pg.K_DOWN]:
            p2.posy -= __MOVE__

        # Player 2 Presses 'DOWN' arrow.
        if keys[pg.K_DOWN] and p2.posy+100 <= 399 and not keys[pg.K_w]:
            p2.posy += __MOVE__

        #---Ball Collisions--------------------#
        # Ball collides with player 1 and is not past the paddle:
        if ball.hitbox.colliderect(p1.hitbox) and ball.hitbox.center[0] > 20:
            ball.velocity[0] = -ball.velocity[0]

            # If the X-Velocity is below __STABLE_VELOCITY__, increase it.
            if ball.velocity[0] < __STABLE_VELOCITY__:
                ball.velocity[0] += 0.1

            # Random increase of Y-Velocity. 50% to be a negative or positive.
            if random.randint(1,2) == 1:
                ball.velocity[1] += random.random()
            else:
                ball.velocity[1] -= random.random()

            randomBallColor(OPS["RANDOMBALL"])
            
        # Ball collides with player 2 and is not past the paddle.
        if ball.hitbox.colliderect(p2.hitbox) and ball.hitbox.center[0] < 380:
            ball.velocity[0] = -ball.velocity[0]

            # If the current X-Velocity is above -__STABLE_VELOCITY__, decrease it further.
            if ball.velocity[0] > -__STABLE_VELOCITY__:
               ball.velocity[0] -= 0.1

            # Random increase of the Y-Velocity. 50% to be negative/positive.
            if random.randint(1,2) == 1:
                ball.velocity[1] += random.random()
            else:
                ball.velocity[1] -= random.random()

            randomBallColor(OPS["RANDOMBALL"])
            
        # Ball collides with the bottom of the screen.
        if ball.hitbox.colliderect(bottomOfScreen) and (ball.hitbox.center[0] > 20 or ball.hitbox.center[0] < 380):
            ball.velocity[1] = -ball.velocity[1]

            if ball.velocity[1] > -__STABLE_Y_VELOCITY__:
                ball.velocity[1] -= 0.15

            randomBallColor(OPS["RANDOMBALL"])
            
        # Ball collides with the top of the screen.
        if ball.hitbox.colliderect(topOfScreen) and (ball.hitbox.center[0] > 20 or ball.hitbox.center[0] < 380):
            ball.velocity[1] = -ball.velocity[1]

            if ball.velocity[1] < __STABLE_Y_VELOCITY__:
                ball.velocity[1] += 0.15

            randomBallColor(OPS["RANDOMBALL"])
            
        #---Score Checking---------------------#
        if p1.score == __MAX_SCORE__:
            
            while RUNNING:
                mPos = pg.mouse.get_pos()

                # Draw the necessary words / rectangles.
                screen.fill((0, 0, 0))
                qButton = pg.Rect((150, 300), (100, 40))
                pg.draw.rect(screen, (255, 0, 0), qButton, 2)
                screen.blit(scorefont.render(("Player 1 wins!"), 1, (0, 255, 255)), (100, 188))

                # If the mouse is in the Quit button, light up the word 'Quit'
                if qButton.collidepoint(mPos) == 1:
                    screen.blit(scorefont.render("Quit", 1, (255, 0, 0)),   (170, 305))
                    screen.blit(scorefont.render("Quit", 1, (255, 0, 255)), (171, 305))
                else:
                    screen.blit(scorefont.render("Quit", 1, (255, 0, 0)), (170, 305))

                pg.display.update()

                for e in pg.event.get():
                    if e.type == pg.QUIT:
                        pg.quit(); sys.exit()

                    elif e.type == pg.MOUSEBUTTONUP and qButton.collidepoint(mPos) == 1:
                        pg.quit(); sys.exit()

        elif p2.score == __MAX_SCORE__:

            while RUNNING:
                mPos = pg.mouse.get_pos()

                # Draw the necessary components and rectangles.
                screen.fill((0, 0, 0))
                qButton = pg.Rect((150, 300), (100, 40))
                pg.draw.rect(screen, (255, 0, 0), qButton, 2)
                screen.blit(scorefont.render(("Player 2 wins!"), 1, (0, 255, 255)), (100, 188))

                # If the mouse is inside the Quit button, make it
                # light up.
                if qButton.collidepoint(mPos) == 1:
                    screen.blit(scorefont.render("Quit", 1, (255, 0, 0)),   (170, 305))
                    screen.blit(scorefont.render("Quit", 1, (255, 0, 255)), (171, 305))
                else:
                    screen.blit(scorefont.render("Quit", 1, (255, 0, 0)), (170, 305))

                pg.display.update()
                
                for e in pg.event.get():
                    if e.type == pg.QUIT:
                        pg.quit(); sys.exit()

                    elif e.type == pg.MOUSEBUTTONUP and qButton.collidepoint(mPos) == 1:
                        pg.quit(); sys.exit()

        #---Player Scoring Mechanic------------#
        # If the ball passes the edge of the screen, on Player 2's side:
        # Increase player 1's score and restart the ball.
        if ball.hitbox.center[0] > 420:
            p1.score += 1

            if p1.score != __MAX_SCORE__:
                ball.sideToGo = __P1SIDE__
                ball.restartBall()

        # If the ball passes the edge of the screen on Player 1's side:
        # Increase player 2's score and restart the ball.
        if ball.hitbox.center[0] < -20:
            p2.score += 1

            if p2.score != __MAX_SCORE__:
                ball.sideToGo = __P2SIDE__
                ball.restartBall()

        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit(); sys.exit()

            # Checks if the 'P' key was pressed to pause the game.
            elif e.type == pg.KEYDOWN and e.key == pg.K_p:
                    RUNNING = False
                    screen.fill((0, 0, 0))
                    screen.blit(scorefont.render("PAUSED", 1, (255, 0, 255)), (155, 195))
                    pg.display.update()

    while not RUNNING:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit(); sys.exit()

            # If the 'P' key is pressed, un-pause the game.
            elif e.type == pg.KEYDOWN and e.key == pg.K_p:
                RUNNING = True

#===End of Program=============================================================#
