# Stellaris Game Information (SGI)
A simple GUI application for reading the state of Stellaris save games written in Python.

Provides these key features:
* Reads basic game information faster than opening Stellaris and loading a save game. 
* Calculates how many years (turns) are left before the victory year.
* Helps plan multiplayer games spanning multiple sessions.

## Inspiration
This program was born out of some minor frustrations:
* The Stellaris load game menu onlys shows the current year, but not the victory year. It's not possible to determine how much of a game is left without loading the game. Both these operations take time. SGI provides this information in seconds.
* After setting the galaxy conditions at the beginning of the game they are not visible from any program menu.
* Other save game tools required too much system configuration, such as the installation of other programming frameworks, and didn't provide a single executible.

## stellaris_save_game_info.ini Definitions
SGI searches for specific strings defined in the stellaris_save_game_info.ini. 
SGI does not parse Stellaris's save game format. 

 Variable | Usage 
------------ | -------------
game_variables_no_tab | Game settings.
galaxy_variables_one_tab | Game galaxy settings.
default_starting_year | The default starting year is 2200.
stellaris_save_game_directory | Change this if necessary.
last_used_save_file | SGI keeps track of the last save file used.

## Required Files 
SGI can be run by either one of two ways:
* Install [Python (tested 3.9)](https://www.python.org) (15 kb)
  1. Download the [main.zip](https://github.com/bai-yi-bai/SGI/archive/refs/heads/main.zip).
  2. Launch the __stellaris_save_game_info.py__ file.
  3. Two files are required: __stellaris_save_game_info.ini__ and __stellaris_save_game_info.py__.
Or
* Download the __stellaris_save_game_info.exe__ release.
