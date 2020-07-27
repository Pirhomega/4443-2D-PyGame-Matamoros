# P01.3 - CovidZAR.EIEIO

## Corbin Matamoros

## Assignment Description

### This program uses the pygame library to move a sprite (textured/colored circle) around a game world while staying centered in the window. The sprite is not allowed to travel off the world (represented by the background image), which is surrounded by white. When the sprite is not moving, the "idle" animation plays. When the sprite hits a boundary,  it plays a "dying" animation

## Folder Structure

|   #   | File | Assignment Description |
| :---: | ----------- | ---------------------- |
|   1    |  [game_pt3.py](game_pt2.py)  | main driver code that lauches Pygame application |
|   2    |  [helper_module.py](helper_module.py)  | helper code written by Dr. Griffin |
|   3    |  [grab_colors.py](grab_colors.py)  | mini program written by Corbin that prints all color options to the `color_list.txt` |
|   4    |  [color_list.txt](color_list.txt)  | list of available window background colors |
|   5    |  [colors.json](colors.json)  | `.json` file of names of colors and their RGB/Hex values |
|   6    |  [ball_48x48.png](ball_48x48.png)  | image used to represent the player in the Pygame application |
|   7    |  [background.jpg](background.jpg)  | image used to represent the world in which the player resides |

## Instructions

1. Ensure the latest version of Python is installed on your system. This code was originally run with Python 3.8.3

2. Follow the instructions on the [pygame wiki](https://www.pygame.org/wiki/GettingStarted) to get it installed.

3. Open a command prompt / terminal in the `P01.3` folder

4. Run `game_pt3.py` by typing `python game_pt3.py title= width= height= startx= starty= fps= player_image= color= background_image=`. Select for yourself the window title (`title`), dimensions in pixels (`width` and `height`), the starting location of your character (`startx` and `starty`), refresh rate (`fps`), your character's image (`player_image`), screen background color (`color`), and the background image (`background_image`). Select the color from [color_list.txt](color_list.txt).

5. To move your player, keep your mouse over the window and move it around (clicking won't do anything). If the mouse leaves the window, the player will stop moving.

6. Close the window to exit the game

## Example

The following is an example of the Pygame app if run with this command: `python game_pt3.py title="Pygame Example" width=1280 height=720 startx=20 starty=20 fps=60 player_image="./ball_48x48.png" color=white background_image="./background.jpg"`

### Gif

![sprite movement video](https://media.giphy.com/media/XyOmBlux6Azs1J3rpu/giphy.gif)

### Screenshots

There are no screenshots. Instead I created a gif above.
