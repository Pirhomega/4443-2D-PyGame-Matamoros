# P02 - Sleigher

## Corbin Matamoros

## Assignment Description

### This program uses the pygame library to move a sprite about one of three levels. Levels are generated based on a text file. Each level has a number of enemies that must be killed and items you must collect before you can progress to the next level. If the player touches an enemy, they die. If they pass all three levels, they win. The game has a starting screen, splash (loading) screen, and a gameover screen.

## Folder Structure

|   #   | File | Assignment Description |
| :---: | ----------- | ---------------------- |
|   1    |  [main.py](main.py)  | main driver code that lauches Pygame application |
|   2    |  [helper_module.py](helper_module.py)  | helper code written by Dr. Griffin |
|   3    |  [resources](./resources)  | Folder containing game assets |
|   4    |  info.json  | a `.json` file found throughout the mob and player asset folders (in [resources](./resources)) of each animations' file name, number of frames in each animation, and speed at which the animation should play |
|   5    |  [info.json](./resources/levels/info.json) | contains the objectives to complete each level, the level that follows, and whether that level is a splash screen or not (life = True if level is a splash screen) |
|   6    |  [helper_scripts](./helper_scripts) | Contains scripts I wrote to rename files and resize images in a folder |

## Instructions

1. Ensure the latest version of Python is installed on your system. This code was originally run with Python 3.8.3

2. Follow the instructions on the [pygame wiki](https://www.pygame.org/wiki/GettingStarted) to get it installed.

3. Open a command prompt / terminal in the `P02` folder

4. Run `main.py` by typing `python main.py title= levels= tile_width= tile_height= width= height= fps= player_images= map_images= mob_images= item_images= sounds=`. Select for yourself the window title (`title`), the location of the level text files (`levels`), the width and height of the tiles used to create the level (`tile_width` and `tile_height`), window width and height (`width` and `height`), refresh rate (`fps`), your character's image folder (`player_images`), the tile images folder (`map_images`), the mob image folder (`mob_images`), the item images folder (`item_images`), and sounds folder (`sounds`).

5. To move your player, use 'd' to move right, 'a' to move left, and SPACE to jump. Use these mechanics to pick up items while avoiding the enemies strewn about. Complete all levels to win the game.

7. Close the window to exit the game

## Example

Here is a example command you can run: `python main.py title="Sleigher" levels="./resources/levels" tile_width=32 tile_height=32 width=25 height=16 fps=30 player_images="./resources/player" map_images="./resources/map_gen" mob_images="./resources/mob" item_images="./resources/item" sounds="./resources/sounds"`
