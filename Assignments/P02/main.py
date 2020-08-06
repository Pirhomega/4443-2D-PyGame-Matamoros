# python main.py title="Pygame Example" level="Level1.txt" tile_width=32 tile_height=32 width=25 height=16 fps=30 player_images="./resources/player" map_images="./resources/map_gen" mob_images="./resources/mob" item_images="./resources/item" sounds="./resources/sounds"
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
from PIL import Image

# Tells OS where to place the window
os.environ['SDL_VIDEO_WINDOW_POS'] = str(460) + "," + str(40)

# helper function that processes commandline arguments into key-value pairs or a list of arguments
from helper_module import mykwargs

# returns the euclidian distance of two points in 2D space
from helper_module import straightDistance

# returns a dictionary of color names and their hex/rgb values
from helper_module import load_json

# grab command line arguments using the helper function and put them into a dictionary
_, ARGDICT = mykwargs(sys.argv)

# constants
TILE_WIDTH = int(ARGDICT['tile_width'])
TILE_HEIGHT = int(ARGDICT['tile_height'])
WINDOW_WIDTH_TILE = int(ARGDICT["width"])
WINDOW_HEIGHT_TILE = int(ARGDICT["height"])
WINDOW_WIDTH = WINDOW_WIDTH_TILE*TILE_WIDTH
WINDOW_HEIGHT = WINDOW_HEIGHT_TILE*TILE_HEIGHT
HALF_WINDOW_WIDTH = int(WINDOW_WIDTH / 2)
HALF_WINDOW_HEIGHT = int(WINDOW_HEIGHT / 2)
WINDOW_TITLE = ARGDICT["title"]
GAME_FPS = int(ARGDICT["fps"])

# each set of sprite animation frames has an info file that contains the names of the frames, how many exist per set,
#       and a value for adjusting the rate each frame plays. For example, if you check the `info.json` file in the `playersprites` folder
#       the player's Idle animation frames all have "Idle (" as part of their name (that's why the 'name' field is "Idle (" ), 
#       and there are 16 frames in the animation. The `fps` parameter has yet to be implemented, but that value just means the next frame
#       will play every 30 iterations of the game's main event loop
player_animations = load_json(ARGDICT["player_images"]+"/info.json")
mob_animations = load_json(ARGDICT["mob_images"]+"/info.json")
# item_animations = load_json(ARGDICT["item_images"]+"/info.json")

class Level(pygame.sprite.Sprite):
    """
    A pygame sprite class visible on screen as an image
    A sprite in pygame is a moveable object on the screen
    The sprite created with this class in this program will be static, acting as the background of the game.
    """
    def __init__(self, level):

        background = Image.open(ARGDICT["map_images"]+"/background.png")
        self.level = []
        self.enemy_locs = []
        self.player_pos = ()
        with open(level,'r') as infile:
            row = 0
            map_data = infile.read()
            map_data = map_data.split("\n")
            for line in map_data:
                col = 0
                sub = []
                for i in range(0,len(line),2):
                    section = line[i]+line[i+1]
                    if '00' in section:
                        sub.append('..')
                        self.enemy_locs.append((col*TILE_WIDTH, (row*TILE_HEIGHT)-TILE_HEIGHT))
                    elif '--' in section:
                        sub.append('..')
                        self.player_pos = (col*TILE_WIDTH, (row*TILE_HEIGHT)-TILE_HEIGHT)
                    elif '14' in section:
                        sub.append('..')
                    elif not '.' in section:
                        sub.append(section)
                        tile = Image.open(ARGDICT["map_images"]+'/'+section+".png").convert("RGBA")
                        tile_top_left = (col*TILE_WIDTH, row*TILE_HEIGHT)
                        # print(tile_top_left)
                        # print(tile)
                        background.paste(tile, box=tile_top_left, mask=tile)
                    else:
                        sub.append(section)
                    col += 1
                self.level.append(sub)
                row += 1
            background.save("level.png", quality=95)
            # print(background)
            # print(level)

        pygame.sprite.Sprite.__init__(self)
        # load the sprite as an image
        self.image = pygame.image.load("level.png").convert()

        # create a pygame rectangle from the dimensions of the background image
        self.rect = self.image.get_rect()

        # place it at 0, 0
        self.rect.topleft = (0, 0)

    # sprite_bottom is a tuple of tuples. It's a tuple of the sprite's bottom left and bottom right corners, which are tuples.
    def getFloor(self, sprite_bottom):
        # grabs the x-coord of the sprite's bottom left and right tuple
        sprite_left = sprite_bottom[0][0] # grabs the x-coord of the bottom left
        sprite_right = sprite_bottom[1][0] # grabs the x-coord of the bottom right
        sprite_row = sprite_bottom[0][1] # grabs the y-coord of the bottom left (could just as well have been the bottom right; they're the same)

        # returns the level matrix location the sprite's bottom left/right corner is in
        sprite_col_l = math.floor(sprite_left / TILE_WIDTH)
        sprite_col_r = math.floor(sprite_right / TILE_WIDTH)
        # the tile the sprite's bottom side sits in
        sprite_row = math.floor((sprite_bottom[0][1]-1) / TILE_HEIGHT)
        # print(sprite_col_l, sprite_col_r, sprite_row)
        for tile in range(sprite_row,WINDOW_HEIGHT_TILE):
            if '.' not in self.level[tile][sprite_col_l] or '.' not in self.level[tile][sprite_col_r]:
                return tile
        return WINDOW_HEIGHT_TILE


class Enemy(pygame.sprite.Sprite):
    """
    A pygame sprite class visible on screen as an image
    A sprite in pygame is a moveable object on the screen
    The sprite created with this class in this program will be unmovable, acting
        as a stationary target for the player character to shoot at. 
    The enemy dies when hit by a Bullet
    """
    def __init__(self, enemy_loc):
        pygame.sprite.Sprite.__init__(self)
        # load the sprite as an image
        # There are two animations that will play in this game: Idle and Dead, located in the `./mob` folder
        # Animations are loop-played, meaning, since each frame of every animation are numbered (e.g. `dead1.png`, `dead2.png`, etc.),
        #       we can loop through them using the `<animation_name>_imagenum` variable. `<animation_name>_imagelimit`
        #       keeps the program from trying to load an image that doesn't exist. (We don't want to open `dead8.png` if
        #       there are only 7 frames in the 'dead' animation.) `<animation_name>_imagelimit` gets its value from the `info.json`
        #       file in the `mob` folder.
        self.idle_imagenum = 1
        self.attack_imagenum = 1
        self.idle_imagelimit = mob_animations["idle"]["count"]
        self.attack_imagelimit = mob_animations["attack"]["count"]
        # this is how we will load any frame of an animation. (Here, we load the first `idle` frame)
        # For example, the first image that loads will be at "./mob/+idle+/+idle+1+.png". I kept the plus signs in so you can see how each part
        #       of the below instruction contributes. The plus's aren't actually in the string.
        self.image = pygame.image.load("./resources/mob/idle/"+str(self.idle_imagenum)+".png")

        # create a pygame rectangle from the dimensions of the image
        self.rect = self.image.get_rect()

        # set the position of the sprite on the window
        #       but don't position the sprite just yet
        self.x, self.y = enemy_loc

        # place the sprite at the location determined above, record its actual position in world coordinates
        self.rect.topleft = self.actual_position = (self.x, self.y)

        # hit will stay true if the sprite has NOT been hit by a Bullet. False, otherwise. We'll use this
        #       variable in the `update` member function
        self.hit = True

    # # adds the offset calculated in the camera class to the enemy's actual position in the world (not with respect to the game window)
    # def update(self, position):

    #     # if the enemy has not been hit by a Bullet, play its 'idle' animation
    #     if self.hit:
    #         # We use the `max` function since there are no animation frames with a 0 in their name,
    #         #       and the mod function will return a 0 if self.<animation>_imagenum = self.<animation>_imagelimit
    #         self.idle_imagenum = max(1, (self.idle_imagenum + 1) % self.idle_imagelimit)
    #         self.image = pygame.image.load("./mob/"+self.idle_pictureset["name"]+'/'+self.idle_pictureset["name"]+str(self.idle_imagenum)+".png")
    #     # if it has been hit
    #     elif not self.hit:
    #         self.dead_imagenum += 1
    #         # if the entire 'dead' animation has played, kill the enemy and remove it from view
    #         if self.dead_imagenum == self.dead_imagelimit:
    #             self.dead_imagenum = 1
    #             self.kill()
    #         # if the animation hasn't finished, play the next frame
    #         else:
    #             self.image = pygame.image.load("./mob/"+self.dead_pictureset["name"]+'/'+self.dead_pictureset["name"]+str(self.dead_imagenum)+".png")

    #     # add the camera offset
    #     self.rect.topleft = (self.actual_position[0]+position[0], self.actual_position[1]+position[1])

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
        # There are three animations that will play in this game: Idle, Dead, and Walk.
        # Animations are loop-played, meaning, since each frame of every animation are numbered (e.g. `Dead (1).png`, `Dead (2).png`, etc.),
        #       we can loop through them using the `<animation_name>_imagenum` variable. `<animation_name>_imagelimit`
        #       keeps the program from trying to load an image that doesn't exist. (We don't want to open `Dead (17).png` if
        #       there are only 16 frames in the Dead animation.) `<animation_name>_imagelimit` gets its value from the `info.json`
        #       file in the `playersprites` folder.
        self.idle_imagenum = 1
        self.dead_imagenum = 1
        self.walk_imagenum = 1
        self.jump_imagenum = 1
        self.idle_imagelimit = player_animations["idle"]["count"]
        self.dead_imagelimit = player_animations["dead"]["count"]
        self.walk_imagelimit = player_animations["walk"]["count"]
        self.jump_imagelimit = player_animations["jump"]["count"]
        # this is how we will load any frame of an animation (here, we load the first frame indicated in the commandline parameters)
        self.image = pygame.image.load(ARGDICT["player_images"]+'/idle/'+str(self.idle_imagenum)+'.png')

        # create a pygame rectangle from the dimensions of the image
        self.rect = self.image.get_rect()
        self.IMAGE_WIDTH = self.rect.right - self.rect.left
        self.IMAGE_HEIGHT = self.rect.bottom - self.rect.top

        # set the position of the sprite on the window in world coordinates
        self.x = int(0*TILE_WIDTH)
        self.y = int(9*TILE_HEIGHT)
        self.old_loc = (0,0)

        # possible states the player can have are 'i' (idle), 'l' (walking left), 'r' (walking right), or 'd' (dying)
        self.state = 'i'
        self.jumping = False
        self.falling = False
        self.vertical_speed = 7
        self.old_vertical_speed = self.vertical_speed
        self.gravity = 5

        # place the sprite at the location determined above, record its actual position in world coordinates,
        #       and lastly record that position as the last viable position it has been in (more on that in this class's
        #       `update` member function)
        self.rect.topleft = self.old_loc = (self.x, self.y)

    def Move(self, floor_y):
        """
        Move controls the position of the sprite by mouse movement
        """
        self.old_loc = self.rect.topleft
        if self.state == 'r':
            if (self.rect.right + 4) <= WINDOW_WIDTH:
                self.x += 4
                self.rect.topleft = (self.x, self.rect.topleft[1])
        if self.state == 'l':
            if (self.rect.left - 4) >= 0:
                self.x -= 4
                self.rect.topleft = (self.x, self.rect.topleft[1])
        if self.jumping:
            # energy = 1/2 * mass * V^2
            energy = self.vertical_speed * self.vertical_speed
            # print("energy:", energy)
            # print("new loc:", self.rect.bottom - energy)
            if self.rect.topleft[1] - energy >= 0:
                # print(self.vertical_speed)
                self.rect.topleft = (self.x, self.rect.topleft[1] - energy)
                self.vertical_speed -= 1
            if self.rect.topleft[1] == 0 or self.vertical_speed == 0:
                self.falling = True
                self.jumping = False
        if self.falling:
            print("We falling!")
            if self.rect.bottom + self.gravity <= floor_y:
                self.rect.bottom += self.gravity
            else:
                self.vertical_speed = self.old_vertical_speed
                self.rect.bottom = floor_y
                self.state = 'i'
                self.falling = False
        if (not self.jumping) and (self.rect.bottom < floor_y):
            self.falling = True


    # applies changes to the player sprite, such as animation and position
    def update(self):
        # If the distance from the mouse to the player is less than 10, loop-play the "Idle" animation, because the player isn't moving
        if self.rect.topleft == self.old_loc:
            self.idle_imagenum = max(1, (self.idle_imagenum + 1) % self.idle_imagelimit)
            self.image = pygame.image.load(ARGDICT["player_images"]+'/idle/'+str(self.idle_imagenum)+'.png')
        # otherwise, loop-play the "Walk" animation
        elif self.state == 'r':
            self.walk_imagenum = max(1, (self.walk_imagenum + 1) % self.walk_imagelimit)
            self.image = pygame.image.load(ARGDICT["player_images"]+'/walk/'+str(self.walk_imagenum)+'.png')
            self.state = 'i'
        elif self.state == 'l':
            self.walk_imagenum = max(1, (self.walk_imagenum + 1) % self.walk_imagelimit)
            image_unrot = pygame.image.load(ARGDICT["player_images"]+'/walk/'+str(self.walk_imagenum)+'.png')
            self.image = pygame.transform.flip(image_unrot, True, False)
            self.state = 'i'
        elif self.state == 'j':
            pass
        elif self.state == 'd':
            pass
        # self.state = 'i'

        # # if the new position of the sprite would put it outside the boundaries of the window, revert to the previous position stored in `self.old_loc`
        # # Also, load the "Dead" animation frames when the player hits a wall
        # if self.actual_position[0] <= 0 or self.actual_position[0]+self.IMAGE_WIDTH >= 1920 or self.actual_position[1] <= 0 or self.actual_position[1]+self.IMAGE_HEIGHT >= 1080:
        #     self.dead_imagenum = max(1, (self.dead_imagenum + 1) % self.dead_imagelimit)
        #     self.image = pygame.image.load("./playersprites/"+self.dead_pictureset["name"]+str(self.dead_imagenum)+").png")
        #     self.actual_position = self.old_loc

def main():
    pygame.init()

    # # initialize the mixer and load the sounds effects
    # pygame.mixer.init(buffer=64)
    # snowball_thrown = pygame.mixer.Sound("./sounds/throw.wav")
    # snowball_hit = pygame.mixer.Sound("./sounds/hit.wav")
    # snowball_thrown.set_volume(0.5)
    # snowball_hit.set_volume(0.5)

    # sets the window title using title found in command line instruction
    pygame.display.set_caption(WINDOW_TITLE)

    # Set up the drawing window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # for controlling frames per second
    clock = pygame.time.Clock()

    # groups for all sprites that are not the player
    main_sprites = pygame.sprite.Group()
    # bullet_sprites = pygame.sprite.Group()
    mob_sprites = pygame.sprite.Group()

    # opening level 1
    level = Level(ARGDICT['level'])
    for loc in level.enemy_locs:
        mob_sprites.add(Enemy(loc))

    # construct the player
    p1 = Player()

    # get how many enemies to spawn in the world from the commandline parameters
    # num_enemies = int(ARGDICT["enemy_count"])


    # construct the background image
    # bkgr = Background()


    # add sprites to the sprite group
    # The order we add these to the group is the order they are drawn to the screen,
    #       so we add the background first to keep the player from being covered
    main_sprites.add(level)
    main_sprites.add(p1)

    # create the enemy objects and add them to the `mob_sprites` group
    # for x in range(num_enemies):
    #     mob_sprites.add(Enemy())

    # Run until the user asks to quit game loop
    running = True
    while running:
        # sets frames per second to what's found in commandline instruction
        clock.tick(GAME_FPS)
        # print(p1.rect.bottomleft, p1.rect.bottomright)
        current_floor = level.getFloor((p1.rect.bottomleft,p1.rect.bottomright))
            # print("This is the tile the player uses as the floor:", current_floor[1])
            # floor_x = current_floor[0]*TILE_WIDTH
        floor_y = current_floor*TILE_HEIGHT
        # print("Current floor", floor_x, floor_y)
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        key_depressed = pygame.key.get_pressed()
        if key_depressed[pygame.K_d]:
            p1.state = 'r'
        if key_depressed[pygame.K_a]:
            p1.state = 'l'
        if key_depressed[pygame.K_SPACE]:
            p1.jumping = True
        p1.Move(floor_y)
            # p1.Move('j', floor_y)
        #     p1.
            # if the user clicks the left mouse button
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     # play the sound of a thrown snowball
            #     snowball_thrown.play()
            #     # create the snowball object
            #     snow_bullet = Bullet(p1.actual_position,mouse_pos)
            #     # add it to the bullet_sprites group
            #     bullet_sprites.add(snow_bullet)

        # focuses in on the player so that it is always centered in the game window
        # camera.update(p1)

        # loop through all sprites in all groups and apply the camera offset to them
        for sprite in main_sprites:
            sprite.update()
        # for sprite in bullet_sprites:
        #     sprite.update(camera.apply())
        # for sprite in mob_sprites:
        #     sprite.update(camera.apply())

        # loop through all bullet and mob sprites and check for collisions between bullets and mobs
        # for bullet in bullet_sprites:
        #     for mob in mob_sprites:
        #         # if a bullet hits a mob
        #         if bullet.rect.colliderect(mob.rect):
        #             # play the sound
        #             snowball_hit.play()
        #             # kill the bullet
        #             bullet.kill()
        #             # switch the mob's hit variable to false so it starts playing its death animation
        #             mob.hit = False

        # # draw the sprites to the screen
        main_sprites.draw(screen)
        # bullet_sprites.draw(screen)
        mob_sprites.draw(screen)
        # show screen
        
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()

if __name__=='__main__':
    main()
