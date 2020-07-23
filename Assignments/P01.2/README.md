# P01.2 - CovidZAR.EIEIO

## Corbin Matamoros

## Assignment Description

### This program uses the pygame library to move a sprite (textured/colored circle) around a game world while staying centered in the window. The sprite is not allowed to travel off the world, which is surrounded by white

## Folder Structure

|   #   | File | Assignment Description |
| :---: | ----------- | ---------------------- |
|   1    |  [game_pt2.py](game_pt2.py)  | main driver code that lauches Pygame application |
|   2    |  [helper_module.py](helper_module.py)  | helper code written by Dr. Griffin |
|   3    |  [color_list.txt](color_list.txt)  | list of available window background colors |
|   4    |  [colors.json](colors.json)  | `.json` file of names of colors and their RGB/Hex values |
|   5    |  [ball_48x48.png](ball_48x48.png)  | image used to represent the player in the Pygame application |
|   6    |  [screenshot1.png](screenshot1.png)  | image showing player in bottom right corner of screen |
|   7    |  [screenshot2.png](screenshot2.png)  | image showing player on left side of screen |
|   8    |  [screenshot3.png](screenshot3.png)  | image showing player at top of screen |

## Instructions

1. Ensure the latest version of Python is installed on your system. This code was originally run with Python 3.8.3

2. Follow the instructions on the [pygame wiki](https://www.pygame.org/wiki/GettingStarted) to get it installed.

3. Open a command prompt / terminal in the `A05.1` folder

4. Run `game.py` by typing `python game.py title= width= height= fps= image= color=`. Select for yourself the Windows title (`title`), dimensions in pixels (`width` and `height`), refresh rate (`fps`), player image (`image`), and screen background color (`color`). Select the color from [color_list.txt](color_list.txt).

5. To move your player, keep your mouse over the window and move it around (clicking won't do anything). If the mouse leaves the window, the player will stop moving.

6. Close the window to exit the game

## Example

The following is an example of the Pygame app if run with this command: `python game.py title="Pygame Example" width=640 height=480 fps=60 image="./ball_48x48.png" color=bisque`

### Gif

![sprite movement video](https://media.giphy.com/media/U6YEDrQ1EzoKWhl9hl/giphy.gif)

### Screenshot 1

<img src="screenshot1.png" width="300">

### Screenshot 2

<img src="screenshot2.png" width="300">

### Screenshot 3

<img src="screenshot3.png" width="300">