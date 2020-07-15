"""
Pygame A05-005

Description:

   Moving a player with Mouse

New Code:

     event.type == pygame.MOUSEBUTTONUP

"""
# Import and initialize the pygame library
import pygame
import random
import sys
import os
import math

# Tells OS where to open the window
os.environ['SDL_VIDEO_WINDOW_POS'] = str(1000) + "," + str(100)

from helper_module import mykwargs
from helper_module import straightDistance

# grab command line arguments
_, argDict = mykwargs(sys.argv)

# from helper_module import load_colors


# # Import pygame.locals for easier access to key coordinates
# # Updated to conform to flake8 and black standards
# from pygame.locals import (
#     K_UP,
#     K_DOWN,
#     K_LEFT,
#     K_RIGHT,
#     K_ESCAPE,
#     KEYDOWN,
#     QUIT,
# )

# config = {
#     'title' :'006 Pygame Lesson',
#     'window_size' : {
#         'width' : 600,
#         'height' : 480
#     }
# }

# colors = load_colors('colors.json')



# class Player:
#     def __init__(self,screen,color,x,y,r):
#         self.screen = screen
#         self.color = color
#         self.x = x
#         self.y = y
#         self.radius = r
#         self.dx = random.choice([-1,1])
#         self.dy = random.choice([-1,1])
#         self.speed = 15
#         self.last_direction = None
#         self.target_location = None
#         self.moving = False

#     def Draw(self):
#         pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

#     def BouncyMove(self):

#         w, h = pygame.display.get_surface().get_size()

#         self.x += (self.speed * self.dx)
#         self.y += (self.speed * self.dy)

#         if self.x <= 0 or self.x >= w:
#             self.dx *= -1

#         if self.y <= 0 or self.y >= h:
#             self.dy *= -1

#     def OnWorld(self):
#         w, h = pygame.display.get_surface().get_size()

#         return self.x > 0 and self.x < w and self.y > 0 and self.y < h

#     def GetDirection(self,keys):
#         if keys[K_UP]:
#             return K_UP
#         elif keys[K_DOWN]:
#             return K_DOWN
#         elif keys[K_LEFT]:
#             return K_LEFT
#         elif keys[K_RIGHT]:
#             return K_RIGHT
#         return None

#     def Move(self):
#         # if len(input) > 2:
#         #     self.MoveWithKeys(input)
#         # if len(input) == 2:
#         #     self.target_location = input
#         #     self.MoveWithMouse()
#         # else:
#         #     self.MoveWithMouse()

#         if self.moving:
#             self.MoveWithMouse()

#     def MouseClicked(self,loc):
#         self.target_location = loc
#         self.moving = True
#         self.MoveWithMouse()
#         print(f"clicked: {loc}")

#     def MoveWithMouse(self):
#         if not self.moving:
#             return
#         x = self.target_location[0]
#         y = self.target_location[1]

#         dx = x - self.x
#         dy = y - self.y
#         angle = math.atan2(dy, dx)

#         if straightDistance(self.x,self.y,x,y) > 10:
#             self.x += int(self.speed * math.cos(angle))
#             self.y += int(self.speed * math.sin(angle))

#     def TelePort(self,input):
#         x = input[0]
#         y = input[1]

#         self.x = x
#         self.y = y

#     def MoveWithKeys(self,keys):
#         self.moving = False
#         direction = self.GetDirection(keys)

#         if self.OnWorld() or direction != self.last_direction:
#             if keys[K_UP]:
#                 self.y -= self.speed
#                 self.last_direction = K_UP
#             elif keys[K_DOWN]:
#                 self.y += self.speed
#                 self.last_direction = K_DOWN
#             elif keys[K_LEFT]:
#                 self.x -= self.speed
#                 self.last_direction = K_LEFT
#             elif keys[K_RIGHT]:
#                 self.x += self.speed
#                 self.last_direction = K_RIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(argDict["image"])
        self.rect = self.image.get_rect()
        self.width = int(argDict["width"])
        self.height = int(argDict["height"])
        self.x = self.width / 2
        self.y = self.height / 2
        self.old_loc = (self.x, self.y)
        self.speed = 5
        self.rect.center = (self.x, self.y)

    def Move(self, mouse_position):
        self.target_location = mouse_position
        self.MoveWithMouse()
        self.rect.center = (self.x, self.y)
        if self.rect.left <= 0 or self.rect.right >= self.width or self.rect.top <= 0 or self.rect.bottom >= self.height:
            print("Too far!")
            self.rect.center = self.old_loc
        print(f"current location at: {self.rect.center}")
        print(f"current left at: {self.rect.left}")
        print(f"old location at: {self.old_loc}")

    def MoveWithMouse(self):
        self.old_loc = self.rect.center

        x = self.target_location[0]
        y = self.target_location[1]

        dx = x - self.x
        dy = y - self.y
        angle = math.atan2(dy, dx)

        if straightDistance(self.x, self.y, x, y) > 10:
            self.x += int(self.speed * math.cos(angle))
            self.y += int(self.speed * math.sin(angle))
        
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

    # group for all sprites
    all_sprites = pygame.sprite.Group()

    # add sprites to the sprite group
    all_sprites.add(p1)

    # Run until the user asks to quit
    # game loop
    running = True
    while running:

        screen.fill((255, 255, 255))

        all_sprites.update()

        # sets frames per second to what's found in commandline instruction
        clock.tick(int(argDict["fps"]))

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if pygame.mouse.get_focused():
            p1.Move(pygame.mouse.get_pos())

        # if pygame.key.get_pressed():
        #     p1.MoveWithKeys(pygame.key.get_pressed())

        # handle MOUSEBUTTONUP

        # p1.Move()
        all_sprites.draw(screen)

        pygame.display.flip()


    # Done! Time to quit.
    pygame.quit()

if __name__=='__main__':
    #colors = fix_colors("colors.json")
    #pprint.pprint(colors)
    main()