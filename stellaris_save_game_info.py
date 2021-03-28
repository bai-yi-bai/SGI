# Stellaris Game Information (SSGI)
# Only requires Python 3.9

import sys
import configparser
import tkinter as tk
import zipfile
import os
import pathlib
import ast
from tkinter import filedialog as fd
import re
from collections import OrderedDict

# pyinstaller command
# pyinstaller -F --noconsole --icon=mag.ico stellaris_save_game_info.py
version = '1.0.0'
default_text = f"Stellaris Game Information (SGI)\t\t\t\tv{version}\nhttps://github.com/bai-yi-bai/SGI"
click_text = """\nClick "Open Save File" to begin.\n\n"""

about_text = """Reads basic game information faster than opening Stellaris. 
Useful for multiplayer games spanning multiple sessions. 
Calculates how many years (turns) are left before victory.

SGI searches for specific strings defined in the stellaris_save_game_info.ini. 
SGI does not parse Stellaris's save game format. 

"game_variables_no_tab"\t\t\t\tGame settings.
"galaxy_variables_one_tab"\t\t\t\tGame galaxy settings.
"default_starting_year"\t\t\t\tThe default starting year is 2200.
"stellaris_save_game_directory"\t\t\t\tChange this if necessary.
"last_used_save_file"\t\t\t\tSGI keeps track fo the last used save.

Stellaris is property of Paradox Interactive https://www.paradoxinteractive.com/

MIT License
Copyright (c) 2021 白一百

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""


# How it works
# 1) Present a file picker
# 2) Treat the .sav file as a .zip
# 3) Open the "gamestate" file from inside the zip
# 4) Search the file for the pre-defined variables
# 6) Display the results in the GUI


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.ui_font = ("Century Gothic", 12, "bold")
        self.dialog_box_default_option = {'font': ("Century Gothic", 12, "bold"),
                                          'foreground': '#%02x%02x%02x' % (29, 197, 124), 'bg': 'black'}
        self.ui_button_options = {'bg': "#2A4038", 'fg': 'white', 'font': ("Century Gothic", 12, "bold")}
        self.master = master
        self.pack()
        self.button_frame = tk.Frame(self, bg='#293731')  # Slightly darker Stellaris green
        self.open_file = tk.Button(self.button_frame, text="Open Save File", command=self.open_file_dialog,
                                   **self.ui_button_options)
        self.about = tk.Button(self.button_frame, text="About", command=self.about, **self.ui_button_options)
        self.quit = tk.Button(self.button_frame, text="Quit", command=self.master.destroy, **self.ui_button_options)
        self.dialog_text_widget = tk.Text(self, width=73, height=40, **self.dialog_box_default_option)
        self.ys = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.dialog_text_widget.yview, )
        self.dialog_text_widget['yscrollcommand'] = self.ys.set
        self.button_frame.grid(column=0, row=0, sticky=tk.EW, columnspan=3)
        self.open_file.grid(column=0, row=0, sticky=tk.W, ipadx=5)
        self.about.grid(column=1, row=0, sticky=tk.W, ipadx=5)
        self.quit.grid(column=2, row=0, sticky=tk.W, ipadx=15)
        self.dialog_text_widget.grid(column=0, row=1, columnspan=2)
        self.ys.grid(column=2, row=1, sticky=tk.NS)
        self.opening_text = 'Click "Open Save File" to begin.'
        self.dialog_text_widget.tag_configure('highlightline', foreground='yellow',
                                              font=self.ui_font, relief='raised')
        self.dialog_text_widget.insert('1.0', default_text)
        self.dialog_text_widget.insert(tk.END, click_text, 'highlightline')

    def about(self):
        self.dialog_text_widget.delete('1.0', tk.END)
        self.dialog_text_widget.insert('1.0', default_text)
        self.dialog_text_widget.insert(tk.END, click_text, 'highlightline')
        self.dialog_text_widget.insert(tk.END, about_text)

    def open_file_dialog(self):
        options = {'defaultextension': '.sav', 'filetypes': [('Stellaris Save', '.sav')], 'initialfile': '',
                   'initialdir': '', 'parent': self, 'title': 'Choose a file'}

        # File picker dialog with last used save
        self.last_used_save_file = config['DEFAULT']['last_used_save_file']
        if self.last_used_save_file == '':  # If first run present the user with the Stellaris save game directory.
            self.last_used_save_file = os.environ['USERPROFILE'] + config.get("DEFAULT",
                                                                              "stellaris_save_game_directory")
            options['initialdir'] = self.last_used_save_file
        else:
            if os.path.isfile(self.last_used_save_file):  # Present the user with the last used file
                options['initialfile'] = pathlib.Path(self.last_used_save_file).name
                options['initialdir'] = pathlib.Path(self.last_used_save_file).parent

        the_file = fd.askopenfile(mode="r", **options)

        if the_file is None:
            self.dialog_text_widget.delete('1.0', tk.END)
            self.dialog_text_widget.insert('1.0', default_text)
            root.update()
        if the_file is not None:
            self.dialog_text_widget.delete('1.0', tk.END)
            self.dialog_text_widget.insert('1.0', f'Reading save game...\n{the_file.name}')
            root.update()

        # Prepare the dictionaries to search for variables
        initial_re_game_dictionary = {variable_name: re.compile(f"\n{variable_name}.*\n".encode()) for variable_name in
                                      game_variables}
        initial_re_game_ordered_dictionary = OrderedDict()
        for item in game_variables:
            initial_re_game_ordered_dictionary[item] = initial_re_game_dictionary[item]
        found_game_dictionary = OrderedDict()
        initial_re_galaxy_dictionary = {variable_name: re.compile(f"\n\t{variable_name}.*\n".encode()) for variable_name
                                        in galaxy_variables}
        initial_re_galaxy_ordered_dictionary = OrderedDict()
        for item in galaxy_variables:
            initial_re_galaxy_ordered_dictionary[item] = initial_re_galaxy_dictionary[item]
        found_galaxy_dictionary = OrderedDict()

        def dictionary_searcher_regex(read_game_state, init_dict, found_dict):
            """Search the game state file using regular expressions"""
            for variable_name in init_dict:
                a_pattern = init_dict[variable_name]
                search_results = a_pattern.search(read_game_state)
                try:  # Clean up and save each variable to the dictionary
                    found_variable = search_results.group().decode('utf-8').replace('\n', '').replace('\t', '').replace(
                        '=', '').replace(variable_name, '').replace('"', '')
                    found_dict[variable_name] = found_variable
                except Exception as regex_e:
                    found_dict[variable_name] = f'NOT FOUND, check syntax. Error: {regex_e}'

        def calculate_game_time_left(found_gal_dict, found_gm_dict):
            """Calculate the time left in the game before the victory year."""
            try:
                victory_year = int(found_gal_dict['victory_year'])
                current_year = int(found_gm_dict["date"][:4])
                end_year = starting_year + victory_year  # 2200 is the default start date
                years_left = end_year - current_year
                found_gm_dict['End Year (Victory)'] = end_year
                found_gm_dict['Years Left'] = years_left
            except Exception as calc_e:
                found_gm_dict['End Year (Victory)'] = f"Could not calculate, error: {calc_e} missing from .ini"
                found_gm_dict['Years Left'] = f"Could not calculate, error: {calc_e} missing from .ini"

        if the_file:  # Save last used file to .ini
            if the_file.name is not None:
                config.set('DEFAULT', 'last_used_save_file', the_file.name)
                config.write(the_config_file.open("w"))

                # Open the save game (zip file)
                treat_as_archive = zipfile.ZipFile(the_file.name, 'r')

                # Open the game state file in the archive
                with treat_as_archive.open('gamestate', 'r') as gamestate:
                    game_state_read = gamestate.read()

                    dictionary_searcher_regex(read_game_state=game_state_read,
                                              init_dict=initial_re_galaxy_ordered_dictionary,
                                              found_dict=found_galaxy_dictionary)

                    dictionary_searcher_regex(read_game_state=game_state_read,
                                              init_dict=initial_re_game_ordered_dictionary,
                                              found_dict=found_game_dictionary)
                    treat_as_archive.close()

                    calculate_game_time_left(found_gm_dict=found_game_dictionary,
                                             found_gal_dict=found_galaxy_dictionary)

                    self.dialog_text_widget.delete('1.0', tk.END)
                    self.dialog_text_widget.insert(tk.END, self.last_used_save_file)
                    self.dialog_text_widget.insert(tk.END, "\nGame Variables")
                    for var in found_game_dictionary.keys():
                        if var == 'Years Left':  # Add highlighting to this

                            self.dialog_text_widget.insert(tk.END,
                                                           f'\n{var}\t\t\t\t{found_game_dictionary[var]}',
                                                           'highlightline')

                        else:
                            self.dialog_text_widget.insert(tk.END,
                                                           f'\n{var}\t\t\t\t{found_game_dictionary[var]}')
                    self.dialog_text_widget.insert(tk.END, "\n\nGalaxy Variables")
                    for var in found_galaxy_dictionary.keys():
                        self.dialog_text_widget.insert(tk.END,
                                                       f'\n{var}\t\t\t\t{found_galaxy_dictionary[var]}')
        if the_file is None:
            self.dialog_text_widget.delete('1.0', tk.END)
            self.dialog_text_widget.insert('1.0', self.opening_text)


def exit_program():
    sys.exit()


def pop_up(text_message):
    root.withdraw()
    window = tk.Toplevel()
    label = tk.Label(window, text=text_message)
    label.pack(fill='x', padx=50, pady=5)
    button_close = tk.Button(window, text="Close", command=exit_program)
    button_close.pack(fill='x')


# Setup Configparser; read the .ini
config = configparser.ConfigParser()

the_config_file_name = 'stellaris_save_game_info.ini'
the_config_file = pathlib.Path(the_config_file_name)

# Build GUI
root = tk.Tk()
root.title("Stellaris Game Information - SGI")
icon_filepath = os.getcwd() + '\\mag.ico'

if os.path.exists(icon_filepath):
    root.iconbitmap(icon_filepath)

if not os.path.exists(the_config_file):
    pop_up(text_message=f'File missing: {the_config_file_name}')

try:
    config.read(the_config_file)

except Exception as e:  # To catch any and all unexpected errors.
    pop_up(text_message=f'Read error: {the_config_file_name}')

try:
    galaxy_variables = ast.literal_eval(config.get("DEFAULT", "galaxy_variables_one_tab"))
    game_variables = ast.literal_eval(config.get("DEFAULT", "game_variables_no_tab"))
    starting_year = int(config.get("DEFAULT", "default_starting_year"))

except Exception as e:  # To catch any and all unexpected errors.
    pop_up(text_message=f'Format error: {the_config_file_name}')

app = Application(master=root)
app.mainloop()
