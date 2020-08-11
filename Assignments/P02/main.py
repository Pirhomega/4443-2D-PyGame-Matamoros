# python main.py title="Pygame Example" levels="./resources/levels" tile_width=32 tile_height=32 width=25 height=16 fps=30 player_images="./resources/player" map_images="./resources/map_gen" mob_images="./resources/mob" item_images="./resources/item" sounds="./resources/sounds" 
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
WINDOW_TITLE = ARGDICT["title"]
GAME_FPS = int(ARGDICT["fps"])

# each set of sprite animation frames has an info file that contains the names of the frames, how many exist per set,
#       and a value for adjusting the rate each frame plays. Since each animation is stored in its own folder, we only need to know
#       how many frames there are and stick that value into the info file. We'll use a loop to iterate through each frame.
player_animations = load_json(ARGDICT["player_images"]+"/info.json")
mob_animations = load_json(ARGDICT["mob_images"]+"/info.json")
level_info = load_json(ARGDICT["levels"]+"/info.json")

class Level(pygame.sprite.Sprite):
    """
    A class that loads a level
    """
    def __init__(self, level):
        # open the level's background image
        background = Image.open(ARGDICT["map_images"]+"/background.png")
        # the level is stored in memory as a 2D array of tiles. The tile dimensions
        #       are given as a command line argument
        self.level = []
        # level objectives are stored here
        self.score_needed = level_info[level]["objectives"]["points"]
        self.enemy_needed = level_info[level]["objectives"]["enemies"]
        # enemies, items, and the player locations are indicated in each level's .txt 
        #       file and their positions are stored here. 
        self.enemy_locs = []
        self.item_locs = []
        self.player_pos = ()
        # this stored all text to be displayed in the level and was sorta hardcoded in...
        #       I was in a rush...
        self.text_locs = []
        # opens the level's .txt file to begin creating it
        with open(ARGDICT["levels"]+'/'+level+'.txt','r') as infile:
            row = 0
            map_data = infile.read()
            map_data = map_data.split("\n")
            # for every line in the .txt file
            for line in map_data:
                col = 0
                sub = []
                # the .txt file is a bunch of two character pairs that represent a part of the level
                # Empty space is '..', enemies are '00', terrain is '01'/'02'/etc., etc.
                for i in range(0,len(line),2):
                    section = line[i]+line[i+1]
                    # if the pair represents anything besides empty space (i.e. '..')
                    if not '.' in section:
                        # if we read in an item
                        if '14' in section:
                            sub.append('..')
                            section = '..'
                            self.item_locs.append((col*TILE_WIDTH, (row*TILE_HEIGHT)))
                        # if we read in an ememy
                        elif '00' in section:
                            sub.append('..')
                            section = '..'
                            self.enemy_locs.append((col*TILE_WIDTH, (row*TILE_HEIGHT)-TILE_HEIGHT))
                        # if we read in the player
                        elif '--' in section:
                            sub.append('..')
                            self.player_pos = (col*TILE_WIDTH, (row*TILE_HEIGHT)-TILE_HEIGHT)
                        # otherwise, we have read in terrain, so fill in the terrain by pasting it to
                        #       the background image
                        else:
                            sub.append(section)
                            tile = Image.open(ARGDICT["map_images"]+'/'+section+".png").convert("RGBA")
                            tile_top_left = (col*TILE_WIDTH, row*TILE_HEIGHT)
                            background.paste(tile, box=tile_top_left, mask=tile)
                    # we read in empty space / air, so just stick it in the array
                    else:
                        sub.append(section)
                    col += 1
                self.level.append(sub)
                row += 1
            # save the background image with the new level tiles pasted on
            background.save("level"+level+".png", quality=95)
            # so now we have a 2D array with each two-character pair stored in each element. We will
            #       use this array when we implement gravity and falling.

        pygame.sprite.Sprite.__init__(self)
        # load the sprite as an image
        self.image = pygame.image.load("level"+level+".png").convert()

        # create a pygame rectangle from the dimensions of the background image
        self.rect = self.image.get_rect()

        # place it at 0, 0
        self.rect.topleft = (0, 0)

    # sprite_bottom is a tuple of tuples. It's a tuple of the sprite's bottom left and bottom right corners, which are tuples.
    # getFloor returns the nearest terrain element stored in the 2D level matrix that is directly under the player's sprite.
    # If the player is falling, the function will loop down from the left and right edges of the sprite
    #       until it either reaches the bottom of the window or a solid block. 
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
        for tile in range(sprite_row,WINDOW_HEIGHT_TILE):
            if '.' not in self.level[tile][sprite_col_l] or '.' not in self.level[tile][sprite_col_r]:
                return tile
        # if the player has nothing under their feet, return the height of the window
        return WINDOW_HEIGHT_TILE


class Enemy(pygame.sprite.Sprite):
    """
    A pygame sprite class visible on screen as an image
    A sprite in pygame is a moveable object on the screen
    The sprite created with this class in this program will be unmovable, 
        but will kill the player if they contact each other
    """
    def __init__(self, enemy_loc):
        pygame.sprite.Sprite.__init__(self)
        # load the sprite as an image
        # There is one animation that will play in this game: Idle, located in the `./resources/mob` folder
        # Animations are loop-played, meaning, since each frame of every animation are numbered (e.g. `dead1.png`, `dead2.png`, etc.),
        #       we can loop through them using the `<animation_name>_imagenum` variable. `<animation_name>_imagelimit`
        #       keeps the program from trying to load an image that doesn't exist. (We don't want to open `8.png` if
        #       there are only 7 frames in the 'dead' animation.) `<animation_name>_imagelimit` gets its value from the `info.json`
        #       file in the `mob` folder.
        self.idle_imagenum = 1
        # self.attack_imagenum = 1
        self.idle_imagelimit = mob_animations["idle"]["count"]
        # self.attack_imagelimit = mob_animations["attack"]["count"]
        # this is how we will load any frame of an animation. (Here, we load the first `idle` frame)
        # For example, the first image that loads will be at "./mob/+idle+/+1+.png". I kept the plus signs in so you can see how each part
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

class Player(pygame.sprite.Sprite):
    """
    A pygame sprite class visible on screen as an image
    A sprite in pygame is a moveable object on the screen
    The sprite created with this class in this program will be moveable with the keyboard
        and will not exit the window boundaries. The mouse must be hovering over the
        window for the sprite to move.
    """
    def __init__(self, player_loc):
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
        # self.jump_imagenum = 1
        self.idle_imagelimit = player_animations["idle"]["count"]
        self.dead_imagelimit = player_animations["dead"]["count"]
        self.walk_imagelimit = player_animations["walk"]["count"]
        # self.jump_imagelimit = player_animations["jump"]["count"]
        # this is how we will load any frame of an animation (here, we load the first frame indicated in the commandline parameters)
        self.image = pygame.image.load(ARGDICT["player_images"]+'/idle/'+str(self.idle_imagenum)+'.png')

        # create a pygame rectangle from the dimensions of the image
        self.rect = self.image.get_rect()

        # set the position of the sprite on the window in world coordinates
        self.x, self.y = player_loc

        # possible states the player can have are 'i' (idle), 'l' (walking left), and 'r' (walking right)
        self.state = 'i'
        # these states are true when the player is jumping, falling, or dying, respectively
        self.jumping = False
        self.falling = False
        self.dying = False
        # how high the player can jump
        self.vertical_speed = 7
        self.old_vertical_speed = self.vertical_speed
        # how fast the player will fall
        self.gravity = 5
        # the player's score
        self.score = 0

        # place the sprite at the location determined above, record its actual position in world coordinates,
        #       and lastly record that position as the last viable position it has been in (more on that in this class's
        #       `update` member function)
        self.rect.topleft = self.old_loc = (self.x, self.y)

    def Move(self, floor_y):
        """
        Move controls the position of the sprite
        """
        self.old_loc = self.rect.topleft
        # if the player is moving to the right
        if self.state == 'r':
            # prevents the player from leaving the window from the right side
            if (self.rect.right + 4) <= WINDOW_WIDTH:
                self.x += 4
                self.rect.topleft = (self.x, self.rect.topleft[1])
        # if the player is moving left
        if self.state == 'l':
            # prevents the player from leaving the window from the left side
            if (self.rect.left - 4) >= 0:
                self.x -= 4
                self.rect.topleft = (self.x, self.rect.topleft[1])
        # if the player is not falling AND is jumping, make them jump
        if self.jumping and not self.falling:
            # calculate the number of pixels to move the player upwards
            energy = self.vertical_speed * self.vertical_speed
            # if the jump won't put us outside the window, move the player upwards
            if self.rect.topleft[1] - energy >= 0:
                self.rect.topleft = (self.x, self.rect.topleft[1] - energy)
                # decrease the jumping speed by one so the jump tapers off
                self.vertical_speed -= 1
            # if the player has hit the top of the window OR the jump speed has reached zero
            #       # switch them from a jumping state to a falling state
            if self.rect.topleft[1] < 0 or self.vertical_speed == 0:
                self.falling = True
                self.jumping = False
        # if the player is falling
        if self.falling:
            # prevent them from falling below the floor (which was determined with the getFloor function)
            if self.rect.bottom + self.gravity <= floor_y:
                self.rect.bottom += self.gravity
            # once the player has reached the floor, reset speed, 
            else:
                self.vertical_speed = self.old_vertical_speed
                # stick the player on th ground
                self.rect.bottom = floor_y
                self.state = 'i'
                self.falling = False
        # this activates the falling state if the player has walked off an edge
        if (not self.jumping) and (self.rect.bottom < floor_y):
            self.falling = True

    # applies changes to the player sprite, such as animation and position
    def update(self):
        # if the player isn't moving, play the idle animation
        if self.rect.topleft == self.old_loc and not self.dying:
            self.idle_imagenum = max(1, (self.idle_imagenum + 1) % self.idle_imagelimit)
            self.image = pygame.image.load(ARGDICT["player_images"]+'/idle/'+str(self.idle_imagenum)+'.png')
        # If the player isn't dying, play the walking right animation
        elif self.state == 'r' and not self.dying:
            self.walk_imagenum = max(1, (self.walk_imagenum + 1) % self.walk_imagelimit)
            self.image = pygame.image.load(ARGDICT["player_images"]+'/walk/'+str(self.walk_imagenum)+'.png')
            self.state = 'i'
        # if the player isn't dying, play the walking left animation (we flip the image of the original frame here)
        elif self.state == 'l' and not self.dying:
            self.walk_imagenum = max(1, (self.walk_imagenum + 1) % self.walk_imagelimit)
            image_unrot = pygame.image.load(ARGDICT["player_images"]+'/walk/'+str(self.walk_imagenum)+'.png')
            self.image = pygame.transform.flip(image_unrot, True, False)
            self.state = 'i'
        # code to play the jumping animation (not done yet)
        elif self.jumping:
            pass
        # if the player's dying state is true, play the dying animation.
        elif self.dying:
            if self.dead_imagenum < self.dead_imagelimit:
                self.dead_imagenum = self.dead_imagenum + 1 % self.dead_imagelimit
                self.image = pygame.image.load(ARGDICT["player_images"]+'/dead/'+str(self.dead_imagenum)+'.png')
            # After playing the entire animation, kill the sprite
            else:
                self.dying = False
                self.kill()

class Item(pygame.sprite.Sprite):
    """
    A pygame sprite class visible on screen as an image
    A sprite in pygame is a moveable object on the screen
    This sprite will act as a collectible for the player
    """
    def __init__(self,item_pos):
        pygame.sprite.Sprite.__init__(self)

        # there's only one sprite image for the item. Load it here.
        self.image = pygame.image.load(ARGDICT["item_images"]+'/1.png')
        # create a pygame rectangle from the dimensions of the image
        self.rect = self.image.get_rect()
        
        # set the position of the sprite on the window
        #       but don't position the sprite just yet
        self.x, self.y = item_pos

        # place the sprite at the location determined above, record its actual position in world coordinates
        self.rect.topleft = (self.x, self.y)

        # hit will stay false if the sprite has NOT been touched by the player. False, otherwise. We'll use this
        #       variable in the `update` member function
        self.hit = False

    def update(self):
        # if the item was contacted by the player, kill it
        if self.hit:
            self.kill()

class LevelInfoHolder():
    '''
    This class will hold all the session information for each level
    '''
    def __init__(self, level_type):
        # set up the background music unless the level is the splash screen
        if level_type != '6':
            pygame.mixer.init(buffer=64)
            self.background_music = pygame.mixer.Sound(ARGDICT["sounds"]+'/'+level_type+'.ogg')
            # the sound was really finicky with volume, so these if/else statements are custom
            #       just to fix that (I think). Did it? Nope...
            if level_type == '2':
                self.background_music.set_volume(0.01)
            else:
                self.background_music.set_volume(0.1)
            self.background_music.play()
        # create sprite groups for the player, mobs, and items
        self.main_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.mob_sprites = pygame.sprite.Group()
        self.level_type = level_type
        # generate the level
        self.level_world = Level(self.level_type)
        # create the player sprite and place them in the level
        self.player = Player(self.level_world.player_pos)
        # place the enemies about the level
        for loc in self.level_world.enemy_locs:
            self.mob_sprites.add(Enemy(loc))
        # place the item about the level
        for loc in self.level_world.item_locs:
            self.item_sprites.add(Item(loc))
        # stick the level and player into the main_sprite's group
        self.main_sprites.add(self.level_world)
        self.main_sprites.add(self.player)
        # if the level is true, it's a splash screen and will only appear for a little bit
        self.temporal = level_info[level_type]["stipulations"]['life']
        # store the next level after this one is passed
        self.next_level = level_info[level_type]["next_level"]

def main():
    pygame.init()

    # initialize the mixer and load the sounds effects
    pygame.mixer.init(buffer=64)
    snowball_hit = pygame.mixer.Sound(ARGDICT["sounds"]+"/hit.ogg")
    santa_death = pygame.mixer.Sound(ARGDICT["sounds"]+"/death.ogg")
    santa_death.set_volume(0.1)
    snowball_hit.set_volume(0.1)

    # sets the window title using title found in command line instruction
    pygame.display.set_caption(WINDOW_TITLE)

    # Set up the drawing window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # for controlling frames per second
    clock = pygame.time.Clock()

    # the level the player is in currently
    current_level = LevelInfoHolder("6")

    # Run until the user asks to quit game loop
    running = True
    while running:
        # sets frames per second to what's found in commandline instruction
        clock.tick(GAME_FPS)

        # grab the nearest floor the player could stand on. If no floor is below, return the window height
        current_floor = current_level.level_world.getFloor((current_level.player.rect.bottomleft,current_level.player.rect.bottomright))
        # convert the floor from number of tiles to pixels
        floor_y = current_floor*TILE_HEIGHT
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        key_depressed = pygame.key.get_pressed()
        # set the state to move the player right
        if key_depressed[pygame.K_d]:
            current_level.player.state = 'r'
        # set the state to move the player left
        if key_depressed[pygame.K_a]:
            current_level.player.state = 'l'
        # set the state to make player jump
        if key_depressed[pygame.K_SPACE]:
            current_level.player.jumping = True
        # actually move the player
        current_level.player.Move(floor_y)

        # loop through all item and mob sprites and check for collisions between items/mob and the player
        for item in current_level.item_sprites:
            # if the player hits an item
            if item.rect.colliderect(current_level.player.rect):
                # play the sound
                snowball_hit.play()
                item.hit = True
                current_level.player.score += 1
        for mob in current_level.mob_sprites:
            if mob.rect.colliderect(current_level.player.rect):
                current_level.background_music.stop()
                santa_death.play()
                current_level.player.dying = True

        # loop through all sprites in all groups and apply the camera offset to them
        for sprite in current_level.main_sprites:
            sprite.update()
        for sprite in current_level.item_sprites:
            sprite.update()

        # # draw the sprites to the screen
        current_level.main_sprites.draw(screen)
        current_level.item_sprites.draw(screen)
        current_level.mob_sprites.draw(screen)
        
        # show screen
        pygame.display.flip()

        # if the gamer has gotten enough canes, move them to the next level
        if current_level.player.score >= current_level.level_world.score_needed:
            current_level.background_music.stop()
            current_level = LevelInfoHolder(current_level.next_level)

        if current_level.temporal:
            current_level = LevelInfoHolder(current_level.next_level)
            pygame.time.wait(2000)
    # Done! Time to quit.
    pygame.quit()

if __name__=='__main__':
    main()
