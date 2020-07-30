# P01.4 - CovidZAR.EIEIO

## Corbin Matamoros

## Assignment Description

### This program uses the pygame library to move a sprite (textured/colored circle) around a game world while staying centered in the window. The sprite is not allowed to travel off the world (represented by the background image), which is surrounded by white. When the sprite is not moving, the "idle" animation plays. When the sprite hits a boundary,  it plays a "dying" animation. The player can also shoot projectiles at randomly dispersed mobs, causing them to explode if hit

## Folder Structure

|   #   | File | Assignment Description |
| :---: | ----------- | ---------------------- |
|   1    |  [game_pt4.py](game_pt2.py)  | main driver code that lauches Pygame application |
|   2    |  [helper_module.py](helper_module.py)  | helper code written by Dr. Griffin |
|   3    |  [grab_colors.py](grab_colors.py)  | mini program written by Corbin that prints all color options to the `color_list.txt` |
|   4    |  [color_list.txt](color_list.txt)  | list of available window background colors |
|   5    |  [colors.json](colors.json)  | `.json` file of names of colors and their RGB/Hex values |
|   6    |  [info.json](./playersprites/info.json)  | a `.json` file of each animations' file name, number of frames in each animation, and speed at which the animation should play |
|   7    |  [background.jpg](background.jpg)  | image used to represent the world in which the player resides |
|   8    |  [playersprites](./playersprites)  | file holding all animations for the player |
|   9    |  [mob](./mob)  | file holding all animations for the enemies/mobs |
|   10   |  [snowball](./snowball)  | file holding all animations for the projectiles the player can throw |
|   11   |  [sounds](./sounds)  | file holding all sounds played in the game |

## Instructions

1. Ensure the latest version of Python is installed on your system. This code was originally run with Python 3.8.3

2. Follow the instructions on the [pygame wiki](https://www.pygame.org/wiki/GettingStarted) to get it installed.

3. Open a command prompt / terminal in the `P01.4` folder

4. Run `game_pt4.py` by typing `python game_pt4.py title= width= height= startx= starty= fps= player_image= color= background_image= enemy_count=`. Select for yourself the window title (`title`), dimensions in pixels (`width` and `height`), the starting location of your character (`startx` and `starty`), refresh rate (`fps`), your character's image (`player_image`), screen background color (`color`), the background image (`background_image`), and the number of enemies to spawn around the world (`enemy_count`). Select the color from [color_list.txt](color_list.txt).

5. To move your player, keep your mouse over the window and move it around (clicking won't do anything). If the mouse leaves the window, the player will stop moving.

6. To throw a snowball at an enemy, click the left mouse button in the direction of the enemy

7. Close the window to exit the game

## Example

The following is an example of the Pygame app if run with this command: `python game_pt4.py title="Pygame Example" width=1280 height=720 startx=2 starty=2 fps=30 player_image="./playersprites/Idle (1).png" color=white background_image="./background.jpg" enemy_count=5`

### Video with sound

[![Sprite Movement Video with Sound](https://img.youtube.com/vi/L64TXapkkA0/0.jpg)](https://www.youtube.com/watch?v=L64TXapkkA0)

### Screenshots

There are no screenshots. Instead I created a gif above.
