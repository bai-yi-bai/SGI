# Stellaris Game Information (SGI)
A simple GUI application for reading the state of Stellaris save games written in Python.

Provides these key features:
* Reads basic game information faster than opening Stellaris and loading a save game. 
* Calculates how many years (turns) are left before the victory year.
* Helps plan multiplayer games spanning multiple sessions.
![SGI](https://user-images.githubusercontent.com/72658127/112743825-42fee200-8fcd-11eb-97b6-111f19e0efa6.png)

## Launching the Application
SGI can be run by either one of two ways:
* Download the [__stellaris_save_game_info v1.0.0.exe__](https://github.com/bai-yi-bai/SGI/releases/tag/v1.0.0) standalone executible release (~9.3 MB).

Or 

1. Install [Python (tested 3.9)](https://www.python.org)
2. Clone the repo or download the main.zip from the __CODE__ button.
3. Launch the __stellaris_save_game_info.py__ file.

## Inspiration
This program was born out of some minor frustrations:
* The Stellaris load game menu onlys shows the current year, but not the victory year. It's not possible to determine how much of a game is left without loading the game. Both these operations take time. SGI provides this information in seconds.
![Stellaris - Save Game Screen](https://user-images.githubusercontent.com/72658127/112743826-43977880-8fcd-11eb-8e27-63d283051080.png)
![SGI - Victory Screen](https://user-images.githubusercontent.com/72658127/112743824-41351e80-8fcd-11eb-87be-9d2de4ff12f5.png)
* After setting the galaxy conditions at the beginning of the game they are not visible from any program menu.
* Other save game tools required too much system configuration, such as the installation of other programming frameworks, and didn't provide a single executible.


## stellaris_save_game_info.ini Definitions
SGI searches for specific strings defined in the stellaris_save_game_info.ini. 
SGI does not parse Stellaris's save game format. It may be possible to search for other strings.

 Variable | Usage 
------------ | -------------
game_variables_no_tab | Game settings.
galaxy_variables_one_tab | Game galaxy settings.
default_starting_year | The default starting year is 2200.
stellaris_save_game_directory | Change this if necessary.
last_used_save_file | SGI keeps track of the last save file used.
