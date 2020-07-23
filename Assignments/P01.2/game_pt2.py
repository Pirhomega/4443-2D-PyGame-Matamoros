# python game_pt2.py title="Pygame Example" width=640 height=480 startx=50 starty=50 fps=60 player_image="./ball_48x48.png" background_image="./background.jpg"
"""
Pygame A05.1

Description:

   Moving a player with Mouse (no clicking necessary) in a large world

"""
# Import and initialize the pygame library
import pygame
import sys
import os
import math

# Tells OS where to open the window
os.environ['SDL_VIDEO_WINDOW_POS'] = str(460) + "," + str(40)

# helper function that processes commandline arguments into key-value pairs or a list of arguments
from helper_module import mykwargs

# returns the euclidian distance of two points in 2D space
from helper_module import straightDistance

# returns a dictionary of color names and their hex/rgb values
from helper_module import load_colors

# grab command line arguments
_, argDict = mykwargs(sys.argv)

# constants
WINDOW_WIDTH = int(argDict["width"])
WINDOW_HEIGHT = int(argDict["height"])
HALF_WINDOW_WIDTH = int(WINDOW_WIDTH / 2)
HALF_WINDOW_HEIGHT = int(WINDOW_HEIGHT / 2)
WINDOW_TITLE = argDict["title"]
GAME_FPS = int(argDict["fps"])

# grab json info from colors.json and load into a dictionary
colors = load_colors('colors.json')

class Camera():
    """
    Used to create an offset in pixels, that when added to all sprites in the game,
    creates a scrolling effect, keeping the targeted sprite in the center of the window
    """
    def __init__(self):
        self.camera_offset = (0,0)

    # moves the camera to focus in on 'target'
    def update(self, player_target):
        # grabs the left and top points of the targeted sprite
        l, t, _, _ = player_target.rect # l = left,  t = top
        # adjusts the camera position based on targeted sprite
        #       subtracting half of the window's width and height gets the distance from the sprite's
        #       current location in the world to the window's center.
        self.camera_offset = (HALF_WINDOW_WIDTH-l, HALF_WINDOW_HEIGHT-t)

    # returns the offset from the update() call to all sprites in the game, including the player.
    # The actual addition doesn't happen in this function, though. It's performed in each sprite's update() class member
    def apply(self):
        # if self.camera_offset[0]+sprite.rect.left <= 0 or self.camera_offset[0]+sprite.rect.right >= 1920 or self.camera_offset[1]+sprite.rect.top <= 0 or self.camera_offset[1]+sprite.rect.bottom >= 1080:
        #     self.camera_offset = (0,0)
        return self.camera_offset


class Background(pygame.sprite.Sprite):
    """
    A pygame sprite class visible on screen as an image
    A sprite in pygame is a moveable object on the screen
    The sprite created with this class in this program will be static, acting as the
        background of the game.
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # load the sprite as an image
        self.image = pygame.image.load(argDict["background_image"]).convert()

        # create a pygame rectangle from the dimensions of the background image
        self.rect = self.image.get_rect()

        # place it at 0, 0
        self.rect.topleft = (0, 0)

    # sets the position of the background with respect to the offset generated in the camera class and passed in as an argument
    # No addition is performed here because the background image was initially placed at 0, 0 and never moves (like the player does)
    def update(self, position):
        self.rect.topleft = (position[0], position[1])

class Player(pygame.sprite.Sprite):
    """
    A pygame sprite class visible on screen as an image
    A sprite in pygame is a moveable object on the screen
    The sprite created with this class in this program will be moveable with the mouse
        and will not exit the window boundaries. The mouse must be hovering over the
        window for the sprite to move.
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # load the sprite as an image
        self.image = pygame.image.load(argDict["player_image"])

        # create a pygame rectable from the dimensions of the image
        self.rect = self.image.get_rect()

        # # set the dimensions of the window as member variables
        # self.width = int(argDict["width"])
        # self.height = int(argDict["height"])

        # set the position of the sprite on the window
        self.x = int(argDict["startx"])
        self.y = int(argDict["starty"])

        # record the previous position of the sprite
        self.old_loc = (self.x, self.y)

        # set how many pixels the sprite will move per frame (fps is set in the commandline)
        self.speed = 5

        # position the sprite on the screen
        self.rect.topleft = self.actual_position = (self.x, self.y)

        # location to which the mouse points
        self.target_location = (0,0)

    def Move(self, mouse_position):
        """
        Move controls the position of the sprite by mouse movement
        """
        # establish the desired position of the sprite
        #   is equal to the mouse's distance from the center of the window plus the actual position of the player
        self.target_location = (mouse_position[0]-HALF_WINDOW_WIDTH+self.actual_position[0], mouse_position[1]-HALF_WINDOW_HEIGHT+self.actual_position[1])
        # calculate the position of the mouse
        self.MoveWithMouse()
        # position the sprite on the screen
        # A distinction has to be made between the sprite's position in the game window (self.rect.topleft) and in the game world (self.actual_position)
        #       The sprite's game window position is what the user sees, but for that positioning to be calculated correctly, the sprite's 
        #       actual position must be remembered.
        self.rect.topleft = self.actual_position = (self.x, self.y)
        # if the new position of the sprite would put it outside the boundaries of the window,
        # revert to the previous position
        if self.rect.left <= 0 or self.rect.right >= 1920 or self.rect.top <= 0 or self.rect.bottom >= 1080:
            self.actual_position = self.old_loc

    def MoveWithMouse(self):
        """
        MoveWithMouse calculates the new position of the sprite based on the
        mouse's position
        """
        # record the current, unchanged position of the sprite
        self.old_loc = self.rect.topleft

        # grabs the x and y coordinate of the mouse's position on the screen
        x = self.target_location[0]
        y = self.target_location[1]

        # find the distance from sprite's current position and desired one
        dx = x - self.x
        dy = y - self.y
        # use the arctan function to find the angle from the horizontal to the desired position
        angle = math.atan2(dy, dx)

        # if the euclidian distance from the original sprite position to the desired is within 10 pixels
        # perform basic trig to move a multiple of `self.speed` towards the desired position
        distance = straightDistance(self.x, self.y, x, y)
        if distance > 10:
            self.x += int(min(5, distance/10) * math.cos(angle))
            self.y += int(min(5, distance/10) * math.sin(angle))

    # adds the offset calculated in the camera class to its actual position in the world (not with respect to the game window)
    def update(self, position):
        self.rect.topleft = (self.actual_position[0]+position[0], self.actual_position[1]+position[1])

def main():
    pygame.init()

    # sets the window title using title found in command line instruction
    pygame.display.set_caption(WINDOW_TITLE)

    # Set up the drawing window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # for controlling frames per second
    clock = pygame.time.Clock()

    # construct the ball
    p1 = Player()

    # construct the background image
    bkgr = Background()

    # construct the camera (image dimensions are hardcoded for now)
    camera = Camera()

    # group for all sprites that are not the player
    all_sprites = pygame.sprite.Group()

    # add sprites to the sprite group
    # The order we add these to the group is the order they are drawn to the screen,
    #       so we add the background first to keep the player from being covered
    all_sprites.add(bkgr)
    all_sprites.add(p1)

    # Run until the user asks to quit game loop
    running = True
    while running:

        # fill screen with white
        screen.fill((255,255,255))

        # sets frames per second to what's found in commandline instruction
        clock.tick(GAME_FPS)

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # attempt to move the player by sending the positioning of the mouse
        if pygame.mouse.get_focused():
            p1.Move(pygame.mouse.get_pos())

        # focuses in on the player so that it is always centered in the game window
        camera.update(p1)

        # loop through all sprites in the group and apply the camera offset to them
        for sprite in all_sprites:
            sprite.update(camera.apply())

        # draw the sprites to the screen
        all_sprites.draw(screen)

        # show screen
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()

if __name__=='__main__':
    main()
