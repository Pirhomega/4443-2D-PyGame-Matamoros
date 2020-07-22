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

# grab json info from colors.json and load into a dictionary
colors = load_colors('colors.json')

class Camera():
    def __init__(self):
        # first establishes the camera position as to look at the entire background
        self.camera_offset = pygame.Rect(0, 0, 1920, 1080)

    # moves the camera to focus in on 'target'
    def update(self, player_target):
        # grabs the left and top points of the targeted sprite
        l, t, _, _ = player_target.rect # l = left,  t = top
        # _, _, w, h = self.camera_position # w = width, h = height
        # adjusts the camera position based on targeted sprite (hardcoded widths and heights; 320, 240, 640, and 480 should actually be
        #       half the camera window width, half camera window height, window width, and window height respectively)
        self.camera_offset = pygame.Rect(l-320, t-240, 1920, 1080)
        # print("This is the camera offset all sprites need to be moved by:")
        # print(self.camera_offset)
        # print(self.camera_offset.topleft)

    def apply(self, target):
        # print(self.camera_offset.topleft)
        # modifier = target.rect.move(self.camera_offset.topleft)
        # print(modifier)
        return self.camera_offset.topleft


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
        print(self.rect)
    
    def update(self, position):
        # print("cam.topleft")
        # print(cam.topleft)
        # print(position)
        self.rect.topleft = (-position[0], -position[1])
        # print(self.rect.topleft)

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

        # set the dimensions of the window as member variables
        self.width = int(argDict["width"])
        self.height = int(argDict["height"])

        # set the position of the sprite on the window
        self.x = int(argDict["startx"])
        self.y = int(argDict["starty"])

        # record the previous position of the sprite
        self.old_loc = (self.x, self.y)

        # set how many pixels the sprite will move per frame (fps is set in the commandline)
        self.speed = 5

        # position the sprite on the screen
        self.rect.center = (self.x, self.y)

    def Move(self, mouse_position):
        """
        Move controls the position of the sprite by mouse movement
        """
        # establish the desired position of the sprite
        self.target_location = mouse_position
        # calculate the position of the mouse
        self.MoveWithMouse()
        # position the sprite on the screen
        self.rect.center = (self.x, self.y)
        # if the new position of the sprite would put it outside the boundaries of the window,
        # revert to the previous position
        if self.rect.left <= 0 or self.rect.right >= self.width or self.rect.top <= 0 or self.rect.bottom >= self.height:
            # print("Too far!")
            self.rect.center = self.old_loc
        # print(f"current location at: {self.rect.center}")
        # print(f"current left at: {self.rect.left}")
        # print(f"old location at: {self.old_loc}")

    def MoveWithMouse(self):
        """
        MoveWithMouse calculates the new position of the sprite based on the
        mouse's position
        """
        # record the current, unchanged position of the sprite
        self.old_loc = self.rect.center

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

def main():
    pygame.init()

    # sets the window title using title found in command line instruction
    pygame.display.set_caption(argDict["title"])

    # Set up the drawing window
    screen = pygame.display.set_mode((int(argDict["width"]), int(argDict["height"])))

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
        # sets frames per second to what's found in commandline instruction
        clock.tick(int(argDict["fps"]))

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # attempt to move the player
        if pygame.mouse.get_focused():
            p1.Move(pygame.mouse.get_pos())

        # focuses in on the player
        camera.update(p1)

        for sprite in all_sprites:
            new_position = camera.apply(sprite)
            sprite.update(new_position)

        # draw the sprites to the screen
        all_sprites.draw(screen)

        # show screen
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()

if __name__=='__main__':
    main()

# fix the direction of the background image