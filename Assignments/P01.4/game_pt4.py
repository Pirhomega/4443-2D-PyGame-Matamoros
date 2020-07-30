# python game_pt4.py title="Pygame Example" width=1280 height=720 startx=20 starty=20 fps=30 player_image="./playersprites/Idle (1).png" color=white background_image="./background.jpg" enemy_count=50
"""
Pygame P01.4

Description:

    Moving a player with Mouse (no clicking necessary) in a large world.
    The camera will move along with the player.
    Player has three animations that play either while moving, staying still, or running into the world border.
    Player can shoot snowballs at surrounding snowmen enemies to kill them.
    Snowballs/Bullets face the correct direction when thrown and have an animation as they fly.
    Snowmen have an idling animation and have a death animation when hit with a snowball.

"""
# Import libraries
import pygame
import sys
import random
import os
import math
import time

# Tells OS where to place the window
os.environ['SDL_VIDEO_WINDOW_POS'] = str(460) + "," + str(40)

# helper function that processes commandline arguments into key-value pairs or a list of arguments
from helper_module import mykwargs

# returns the euclidian distance of two points in 2D space
from helper_module import straightDistance

# returns a dictionary of color names and their hex/rgb values
from helper_module import load_json

# grab command line arguments using the helper function and put them into a dictionary
_, argDict = mykwargs(sys.argv)

# constants
WINDOW_WIDTH = int(argDict["width"])
WINDOW_HEIGHT = int(argDict["height"])
HALF_WINDOW_WIDTH = int(WINDOW_WIDTH / 2)
HALF_WINDOW_HEIGHT = int(WINDOW_HEIGHT / 2)
WINDOW_TITLE = argDict["title"]
GAME_FPS = int(argDict["fps"])

# grab json info from colors.json and load into a dictionary
colors = load_json('colors.json')

# each set of sprite animation frames has an info file that contains the names of the frames, how many exist per set,
#       and a value for adjusting the rate each frame plays. For example, if you check the `info.json` file in the `playersprites` folder
#       the player's Idle animation frames all have "Idle (" as part of their name (that's why the 'name' field is "Idle (" ), 
#       and there are 16 frames in the animation. The `fps` parameter has yet to be implemented, but that value just means the next frame
#       will play every 30 iterations of the game's main event loop
player_animations = load_json('./playersprites/info.json')
mob_animations = load_json('./mob/info.json')
bullet_animations = load_json('./snowball/info.json')

class Camera():
    """
    Used to create an offset in pixels, that when added to all sprites in the game,
    creates a scrolling effect, keeping the targeted sprite in the center of the window.
    Users can pass in whatever sprite they want centered on when they call the `update` function.
    The `apply` function must then be called on every sprite (including the one you called `update`
    with) to apply the offset.
    """
    def __init__(self):
        self.camera_offset = (0,0)

    # moves the camera to focus in on 'target'
    def update(self, player_target):
        # grabs the left and top points of the targeted sprite
        l, t = player_target.actual_position # l = left,  t = top
        # adjusts the camera position based on targeted sprite
        #       subtracting half of the window's width and height gets the distance from the sprite's
        #       current location in the world to the window's center.
        self.camera_offset = (HALF_WINDOW_WIDTH-l, HALF_WINDOW_HEIGHT-t)

    # returns the offset from the update() call to all sprites in the game, including the player.
    # The actual addition doesn't happen in this function, though. It's performed in each sprite's update() class member
    def apply(self):
        return self.camera_offset

class Background(pygame.sprite.Sprite):
    """
    A pygame sprite class visible on screen as an image
    A sprite in pygame is a moveable object on the screen
    The sprite created with this class in this program will be static, acting as the background of the game.
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # load the sprite as an image
        self.image = pygame.image.load(argDict["background_image"]).convert()

        # create a pygame rectangle from the dimensions of the background image
        self.rect = self.image.get_rect()

        # place it at 0, 0
        self.rect.topleft = (0, 0)

    # The update method for sprites doesn't do anything unless defined by the programmer.
    # Sets the position of the background with respect to the offset generated in the camera class and passed in as an argument
    # No addition is performed here because the background image was initially placed at 0, 0 and never moves
    def update(self, position):
        self.rect.topleft = (position[0], position[1])

class Enemy(pygame.sprite.Sprite):
    """
    A pygame sprite class visible on screen as an image
    A sprite in pygame is a moveable object on the screen
    The sprite created with this class in this program will be unmovable, acting
        as a stationary target for the player character to shoot at. 
    The enemy dies when hit by a Bullet
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # the current set of sprite images to use
        self.dead_pictureset = mob_animations["Dead"]
        self.idle_pictureset = mob_animations["Idle"]

        # load the sprite as an image
        # There are two animations that will play in this game: Idle and Dead, located in the `./mob` folder
        # Animations are loop-played, meaning, since each frame of every animation are numbered (e.g. `dead1.png`, `dead2.png`, etc.),
        #       we can loop through them using the `<animation_name>_imagenum` variable. `<animation_name>_imagelimit`
        #       keeps the program from trying to load an image that doesn't exist. (We don't want to open `dead8.png` if
        #       there are only 7 frames in the 'dead' animation.) `<animation_name>_imagelimit` gets its value from the `info.json`
        #       file in the `mob` folder.
        self.idle_imagenum = 1
        self.dead_imagenum = 0
        self.idle_imagelimit = self.idle_pictureset["count"]
        self.dead_imagelimit = self.dead_pictureset["count"]
        # this is how we will load any frame of an animation. (Here, we load the first `idle` frame)
        # For example, the first image that loads will be at "./mob/+idle+/+idle+1+.png". I kept the plus signs in so you can see how each part
        #       of the below instruction contributes. The plus's aren't actually in the string.
        self.image = pygame.image.load("./mob/"+self.idle_pictureset["name"]+'/'+self.idle_pictureset["name"]+str(self.idle_imagenum)+".png")

        # create a pygame rectangle from the dimensions of the image
        self.rect = self.image.get_rect()

        # set the position of the sprite on the window
        #       but don't position the sprite just yet
        self.x = random.randint(0,WINDOW_WIDTH)
        self.y = random.randint(0,WINDOW_HEIGHT)

        # place the sprite at the location determined above, record its actual position in world coordinates
        self.rect.topleft = self.actual_position = (self.x, self.y)

        # hit will stay true if the sprite has NOT been hit by a Bullet. False, otherwise. We'll use this
        #       variable in the `update` member function
        self.hit = True

    # adds the offset calculated in the camera class to the enemy's actual position in the world (not with respect to the game window)
    def update(self, position):

        # if the enemy has not been hit by a Bullet, play its 'idle' animation
        if self.hit:
            # We use the `max` function since there are no animation frames with a 0 in their name,
            #       and the mod function will return a 0 if self.<animation>_imagenum = self.<animation>_imagelimit
            self.idle_imagenum = max(1, (self.idle_imagenum + 1) % self.idle_imagelimit)
            self.image = pygame.image.load("./mob/"+self.idle_pictureset["name"]+'/'+self.idle_pictureset["name"]+str(self.idle_imagenum)+".png")
        # if it has been hit
        elif not self.hit:
            self.dead_imagenum += 1
            # if the entire 'dead' animation has played, kill the enemy and remove it from view
            if self.dead_imagenum == self.dead_imagelimit:
                self.dead_imagenum = 1
                self.kill()
            # if the animation hasn't finished, play the next frame
            else:
                self.image = pygame.image.load("./mob/"+self.dead_pictureset["name"]+'/'+self.dead_pictureset["name"]+str(self.dead_imagenum)+".png")

        # add the camera offset
        self.rect.topleft = (self.actual_position[0]+position[0], self.actual_position[1]+position[1])

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

        # the current set of sprite images to use for the player's animations
        self.idle_pictureset = player_animations["Idle"]
        self.dead_pictureset = player_animations["Dead"]
        self.walk_pictureset = player_animations["Walk"]

        # load the sprite as an image
        # There are three animations that will play in this game: Idle, Dead, and Walk.
        # Animations are loop-played, meaning, since each frame of every animation are numbered (e.g. `Dead (1).png`, `Dead (2).png`, etc.),
        #       we can loop through them using the `<animation_name>_imagenum` variable. `<animation_name>_imagelimit`
        #       keeps the program from trying to load an image that doesn't exist. (We don't want to open `Dead (17).png` if
        #       there are only 16 frames in the Dead animation.) `<animation_name>_imagelimit` gets its value from the `info.json`
        #       file in the `playersprites` folder.
        self.idle_imagenum = 1
        self.dead_imagenum = 1
        self.walk_imagenum = 1
        self.idle_imagelimit = self.idle_pictureset["count"]
        self.dead_imagelimit = self.dead_pictureset["count"]
        self.walk_imagelimit = self.walk_pictureset["count"]
        # this is how we will load any frame of an animation (here, we load the first frame indicated in the commandline parameters)
        self.image = pygame.image.load(argDict["player_image"])

        # create a pygame rectangle from the dimensions of the image
        self.rect = self.image.get_rect()
        self.IMAGE_WIDTH = self.rect.right - self.rect.left
        self.IMAGE_HEIGHT = self.rect.bottom - self.rect.top

        # set the position of the sprite on the window in world coordinates
        self.x = int(argDict["startx"])
        self.y = int(argDict["starty"])

        # place the sprite at the location determined above, record its actual position in world coordinates,
        #       and lastly record that position as the last viable position it has been in (more on that in this class's
        #       `update` member function)
        self.rect.topleft = self.actual_position = self.old_loc = (self.x, self.y)

        # distance is from the mouse pointer to the sprite's topleft corner
        # speed is how fast the player sprite will travel across the screen
        self.distance = 0
        self.speed = 5

        # location to which the mouse points
        self.target_location = (0,0)

    def Move(self, mouse_position):
        """
        Move controls the position of the sprite by mouse movement
        """
        # establish the desired position of the sprite
        #   is equal to the mouse's distance from the center of the window plus the actual position of the player in world coordinates
        world_coord_x = mouse_position[0]-HALF_WINDOW_WIDTH+self.actual_position[0]
        world_coord_y = mouse_position[1]-HALF_WINDOW_HEIGHT+self.actual_position[1]
        self.target_location = (world_coord_x,world_coord_y)

        # calculate the position of the mouse
        self.MoveWithMouse()

        # A distinction has to be made between the sprite's position in the game window (self.rect.topleft) and in the game world (self.actual_position)
        #       The sprite's game window position is what the user sees, but for that positioning to be calculated correctly, the sprite's
        #       actual position must be remembered.
        self.actual_position = (self.x, self.y)

    def MoveWithMouse(self):
        """
        MoveWithMouse calculates the new position of the sprite based on the
        mouse's position
        """
        # record the current, unchanged position of the sprite
        # self.old_loc = self.rect.topleft
        self.old_loc = self.actual_position # okay doing this one actually plays the dead animation, but the camera still follows an invisible santa into the void

        # grabs the x and y coordinate of the mouse's position on the screen
        x = self.target_location[0]
        y = self.target_location[1]

        # find the distance from sprite's current position and desired one
        dx = x - self.x
        dy = y - self.y

        # use the arctan function to find the angle from the horizontal to the desired position
        angle = math.atan2(dy, dx)

        # perform basic trig to move a multiple of `self.speed` towards the desired position
        # Using "min(5, self.distance/10)" lets the sprite move at a speed of 5 to self.distance/10,
        #       so that its speed is a function of the distance from it to the mouse
        self.distance = straightDistance(self.x, self.y, x, y)
        self.x += int(min(5, self.distance/10) * math.cos(angle))
        self.y += int(min(5, self.distance/10) * math.sin(angle))

    # applies changes to the player sprite, such as animation and position
    def update(self, position):
        # If the distance from the mouse to the player is less than 10, loop-play the "Idle" animation, because the player isn't moving
        if self.distance < 10:
            self.idle_imagenum = max(1, (self.idle_imagenum + 1) % self.idle_imagelimit)
            self.image = pygame.image.load("./playersprites/"+self.idle_pictureset["name"]+str(self.idle_imagenum)+").png")
        # otherwise, loop-play the "Walk" animation
        elif self.distance >= 10:
            self.walk_imagenum = max(1, (self.walk_imagenum + 1) % self.walk_imagelimit)
            self.image = pygame.image.load("./playersprites/"+self.walk_pictureset["name"]+str(self.walk_imagenum)+").png")

        # if the new position of the sprite would put it outside the boundaries of the window, revert to the previous position stored in `self.old_loc`
        # Also, load the "Dead" animation frames when the player hits a wall
        if self.actual_position[0] <= 0 or self.actual_position[0]+self.IMAGE_WIDTH >= 1920 or self.actual_position[1] <= 0 or self.actual_position[1]+self.IMAGE_HEIGHT >= 1080:
            self.dead_imagenum = max(1, (self.dead_imagenum + 1) % self.dead_imagelimit)
            self.image = pygame.image.load("./playersprites/"+self.dead_pictureset["name"]+str(self.dead_imagenum)+").png")
            self.actual_position = self.old_loc
        # add the camera offset to the player sprite's actual position in the game world, "moving" them to the center of the window
        self.rect.topleft = (self.actual_position[0]+position[0], self.actual_position[1]+position[1])

class Bullet(pygame.sprite.Sprite):
    """
    A pygame sprite class visible on screen as an image
    A sprite in pygame is a moveable object on the screen
    The sprite created with this class in this program will be move in a straight line
        toward the mouse pointer's position when the mouse left button is clicked.
        If the bullet comes in contact with a mob, the mob dies.
    """
    def __init__(self,player_pos,mouse_pos):
        pygame.sprite.Sprite.__init__(self)

        # the current set of sprite images to use
        self.bullet_pictureset = bullet_animations["Shot"]

        # load the sprite as an image
        # There are three animations that will play in this game: Idle, Dead, and Walk.
        # Animations are loop-played, meaning, since each frame of every animation are numbered (e.g. `Dead (1).png`, `Dead (2).png`, etc.),
        #       we can loop through them using the `<animation_name>_imagenum` variable. `<animation_name>_imagelimit`
        #       keeps the program from trying to load an image that doesn't exist. (We don't want to open `Dead (17).png` if
        #       there are only 16 frames in the Dead animation.) `<animation_name>_imagelimit` gets its value from the `info.json`
        #       file in the `playersprites` folder.
        self.bullet_imagenum = 1
        self.bullet_imagelimit = self.bullet_pictureset["count"]
        # this is how we will load any frame of an animation (here, we load the first `Idle` frame).
        # Here, we save the upright, unrotated version of the sprite (we want to rotate it so that it faces the direction it's shot at)
        self.image_unrot = pygame.image.load("./snowball/"+self.bullet_pictureset["name"]+str(self.bullet_imagenum)+".png")
        
        # create a pygame rectangle from the dimensions of the image
        self.rect = self.image_unrot.get_rect()

        # angle between the horizontal and the mouse pointer.
        # Using the same trigonometry to move the player sprite, we will save the angle the bullet will
        #       fly at.
        self.angle = self.getBulletDirection(mouse_pos)

        # rotate the sprite to face the direction saved in `self.angle`. We convert it from radians to degrees
        #       and add 180 to it (because when I did the math, bullets were facing the opposite direction)
        self.image = pygame.transform.rotate(self.image_unrot, (self.angle*57.29578)+180)

        # set the position of the sprite on the window
        self.x = player_pos[0]
        self.y = player_pos[1]

        # position the sprite and record it's actual position (world coords)
        self.rect.topleft = self.actual_position = (self.x, self.y)

    def getBulletDirection(self, mouse_pos):
        """
        MoveWithMouse calculates the new position of the sprite based on the
        mouse's position
        """
        # grabs the x and y coordinate of the mouse's position on the screen
        x = mouse_pos[0]
        y = mouse_pos[1]

        # find the distance from sprite's current position and desired one
        dx = x - HALF_WINDOW_WIDTH
        dy = y - HALF_WINDOW_HEIGHT
        
        # use the arctan function to find the angle from the horizontal to the desired position
        return math.atan2(dy, dx)

    # adds the offset calculated in the camera class to its actual position in the world (not with respect to the game window)
    def update(self, position):
        # get next frame of the bullet animation
        self.bullet_imagenum = max(1, (self.bullet_imagenum + 1) % self.bullet_imagelimit)
        self.image_unrot = pygame.image.load("./snowball/"+self.bullet_pictureset["name"]+str(self.bullet_imagenum)+".png")

        # rotate the bullet to face the right direction and load
        self.image = pygame.transform.rotate(self.image_unrot, (self.angle*-57.29578)+180)
        
        # adjust the position of the bullet with respect to the `self.angle`. Speed of bullet is "10"
        self.x += int(10 * math.cos(self.angle))
        self.y += int(10 * math.sin(self.angle))

        # save new position in world coords
        self.actual_position = (self.x,self.y)
        # if the new position of the sprite would put it outside the boundaries of the window,
        #       kill the sprite
        if self.actual_position[0] <= 0 or self.actual_position[0] >= 1920 or self.actual_position[1] <= 0 or self.actual_position[1] >= 1080:
            self.kill()
        # add the camera offset to the player sprite's actual position in the game world, "moving" them to the center of the window
        else:
            self.rect.topleft = (self.actual_position[0]+position[0], self.actual_position[1]+position[1])

def main():
    pygame.init()

    # initialize the mixer and load the sounds effects
    pygame.mixer.init(buffer=64)
    snowball_thrown = pygame.mixer.Sound("./sounds/throw.wav")
    snowball_hit = pygame.mixer.Sound("./sounds/hit.wav")
    snowball_thrown.set_volume(0.5)
    snowball_hit.set_volume(0.5)

    # sets the window title using title found in command line instruction
    pygame.display.set_caption(WINDOW_TITLE)

    # Set up the drawing window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # for controlling frames per second
    clock = pygame.time.Clock()

    # get how many enemies to spawn in the world from the commandline parameters
    num_enemies = int(argDict["enemy_count"])

    # construct the ball
    p1 = Player()

    # construct the background image
    bkgr = Background()

    # construct the camera
    camera = Camera()

    # groups for all sprites that are not the player
    main_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    mob_sprites = pygame.sprite.Group()

    # add sprites to the sprite group
    # The order we add these to the group is the order they are drawn to the screen,
    #       so we add the background first to keep the player from being covered
    main_sprites.add(bkgr)
    main_sprites.add(p1)

    # create the enemy objects and add them to the `mob_sprites` group
    for x in range(num_enemies):
        mob_sprites.add(Enemy())

    # Run until the user asks to quit game loop
    running = True
    while running:

        # fill screen with color from commandline
        screen.fill(colors[argDict["color"]]['rgb'])

        # sets frames per second to what's found in commandline instruction
        clock.tick(GAME_FPS)

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # if the user clicks the left mouse button
            if event.type == pygame.MOUSEBUTTONDOWN:
                # play the sound of a thrown snowball
                snowball_thrown.play()
                # create the snowball object
                snow_bullet = Bullet(p1.actual_position,mouse_pos)
                # add it to the bullet_sprites group
                bullet_sprites.add(snow_bullet)

        # attempt to move the player by sending the positioning of the mouse
        if pygame.mouse.get_focused():
            mouse_pos = pygame.mouse.get_pos()
            p1.Move(mouse_pos)

        # focuses in on the player so that it is always centered in the game window
        camera.update(p1)

        # loop through all sprites in all groups and apply the camera offset to them
        for sprite in main_sprites:
            sprite.update(camera.apply())
        for sprite in bullet_sprites:
            sprite.update(camera.apply())
        for sprite in mob_sprites:
            sprite.update(camera.apply())

        # loop through all bullet and mob sprites and check for collisions between bullets and mobs
        for bullet in bullet_sprites:
            for mob in mob_sprites:
                # if a bullet hits a mob
                if bullet.rect.colliderect(mob.rect):
                    # play the sound
                    snowball_hit.play()
                    # kill the bullet
                    bullet.kill()
                    # switch the mob's hit variable to false so it starts playing its death animation
                    mob.hit = False

        # draw the sprites to the screen
        main_sprites.draw(screen)
        bullet_sprites.draw(screen)
        mob_sprites.draw(screen)
        # show screen
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()

if __name__=='__main__':
    main()
