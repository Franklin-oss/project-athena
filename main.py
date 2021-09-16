"""
Project Athena - Alpha Version 0.2
-------------------------------------------------------
Project Athena is a program dreamt up in the genius mind of Franklin, intended to make brilliant workbook solving, a heck of a lot easier.
It has been in the works for months but only recently has it been in active development as the author like completely forgot about it for a few months.
It is built in the hopes that it will make life a lot easier and make brilliant bearable
Please do note that this program is only intended to be used as a last resort incase the user was not able to finish their workbook on time.
Please do not use this as a substitute for studying at all as it is almost certain that you will not have this program to assist you when it is time to write JEE/NEET
or whichever exam it is you are preparing for. With that in mind, enjoy! 
"""
# Imports
import os
import time
import getpass
import platform
from simple_term_menu import TerminalMenu
import json
import extractor
import selenium_basic_v1

# TODO: Use chromedriver autoinstaller
# TODO: Use temp GUI for path selection


VERSION = 0.2
STATE = 'Alpha'


class Interface:
    def __init__(self):
        """
        Initialize interface object
        """
        self.main_menu_title = f"Project Athena v{VERSION}- {STATE}. Built by LaFrnksta356"

        # Set command to clear terminal depending on which OS the program is running on
        if platform.system() == 'Windows':
            self.clear_com = 'cls'
        else:
            self.clear_com = 'clear'

        self.clear = lambda: os.system(self.clear_com)  # Lambda to clear the screen
        self.fhandler = file_handler()  # Initialize file handler

        self.main_screen()

    def main_screen(self):
        """
        Display the main screen with menu
        """
        self.clear()

        def main_menu():
            options = ['[1] Start Solving', '[2] How to use', '[3] Set pdf file','[4] Settings', '[5] Exit']
            main_menu = TerminalMenu(options)
            inp = main_menu.show()  # Show the menu and fetch input

            return inp

        inp = main_menu()

        if inp + 1 == 1:  
            self.solve_ui() # Start solve UI + warnings
        
        elif inp + 1 == 2:
            self.how_to_use_ui()

        elif inp + 1 == 3:
            self.set_paths_UI()
            self.main_screen()

        elif inp + 1 == 4:
            self.settings_ui()
        
        elif inp + 1 == 5:
            exit()

    
    def how_to_use_ui(self):
        self.clear()
        print('Blank lol')
        input()
        self.main_screen()

    def settings_ui(self):
        """
        UI to change settings
        """
        self.clear()

        current_settings = self.fhandler.read_settings()  # Read current settings
        
        options = list(self.fhandler.default_settings.keys())  # List all available settings in options
        settings_menu = TerminalMenu(options)

        selection_idx = settings_menu.show()  # Show menu
        selection = options[selection_idx]

        inp = input(f'What value to set it to? {selection} is currently set to [{current_settings[selection]}] (Enter q to cancel) \n> ')
        if inp.upper() == 'Q':
            self.main_screen()

        self.fhandler.change_settings(selection, inp)

        print('Value has been set sucessfully. Press enter to proceed to main menu')
        input()

        self.main_screen()
        

    def set_paths_UI(self):
        """
        Function to make sure paths for pdf file and chromedriver are set
        """

        self.clear()

        settings = self.fhandler.read_settings()
        pdfpath = settings['pdf_file_path']

        print(f'File path is currently set to: {pdfpath}')
        print('Select pdf file for workbook:')

        from tkinter import Tk     # from tkinter import Tk for Python 3.x
        from tkinter.filedialog import askopenfilename

        Tk().withdraw()  # don't want a full GUI, so keep the root window from appearing
        filepath = askopenfilename()  # show an "Open" dialog box and return the path to the selected file

        if filepath == []:  # If file path is empty restart func
            self.set_paths_UI()

        self.fhandler.change_settings('pdf_file_path', filepath)



    def solve_ui(self):
        self.clear()

        settings = self.fhandler.read_settings() 
        if settings['pdf_file_path'] == [] or not os.path.isfile(settings['pdf_file_path']):  # becomes [] when blank idk why
            self.set_paths_UI()

        print(f"""
        Input pdf file is currently: {settings['pdf_file_path']}
        Start solving? (Y/n). M to go back to main menu. Ctrl + C to quit \n
        """)
        
        inp = input('> ').upper()
        if inp != 'Y':  # Go back to main screen if not Y
            self.main_screen()
    
        start_pg = int(input("Enter start page (at which page in the pdf the chapter starts): \n"))
        end_pg = int(input("Enter end page (last page of the chapter you want to solve): \n"))
        
        print('Start script? Make sure to keep your hands off while it does its thing. Definitely do NOT close the chrome window it opens up. \n')
        if input('Press enter to start or press m and then enter to go back. Ctrl + C to quit \n \n').upper() == 'M':
            self.main_screen()

        # Extract the questions
        ext = extractor.Extractor(settings['pdf_file_path'], (start_pg, end_pg))
        qlist = ext.extract_questions()

        # Open the browser tabs
        hdl = selenium_basic_v1.browser_handle(qlist)
        hdl.open_tabs()

        



class file_handler:
    """
    Handles file interactions and settings from JSON file
    """

    def __init__(self):
        user = getpass.getuser()  # Fetch current username
        if platform.system() == 'Linux':
            self.appdata_path = f'/home/{user}/.lafrnksta_356/'  # Always leave a slash at the end (else it will break the settings path addition)
        elif platform.system() == 'Windows':
            self.appdata_path = f'C:\\Users\\{user}\\AppData\\LaFrnksta356\\'
        elif platform.system() == 'Darwin':
            raise Exception('Goddamn macOS. Ill code it for you later.')

        if not os.path.isdir(self.appdata_path):  # Make the appdata directory if it does not exist
            os.mkdir(self.appdata_path)  

        self.default_settings = {
            'pdf_file_path': 'not set',
            'open_direct_links': False,
        }

        self.settings_path = self.appdata_path + 'settings.json'


    def generate_settings_file(self) -> dict:
        """
        Generate settings json file for the first time with default settings
        """
        with open(self.settings_path, 'w') as sfile:
            sfile.write(json.dumps(self.default_settings))
        
        return self.default_settings  # Return the def settings so that program can pull it directly instead of calling it again
    

    def read_settings(self) -> dict:
        """
        Read and return saved settings from the settings file
        """
        try:
            with open(self.settings_path, 'r') as file:
                return json.loads(file.read())  # Return json converted into dict
        
        except FileNotFoundError:  # Handle if file does not exist
            return self.generate_settings_file()  # Return the default settings after generating settings file instead of calling it again


    def change_settings(self, setting: str, value) -> dict:
        """
        Change the value of one of the settings in the file and return the new dict

        Args:
            setting (str): The setting to be changed
            value ([type]): Value that setting is to be changed to

        Returns:
            dict: New settings dict
        """

        settings = self.read_settings()
        settings[setting] = value
        try:
            with open(self.settings_path, 'w') as file:
                file.write(json.dumps(settings))  # Write the new changed dict into the file after converting to json
            
            return settings

        except FileNotFoundError:
            raise FileNotFoundError('The settings file does not exist. Please generate a new file in settings and then change it.')
    

    def log_qlist(qlist: list):
        """
        Log questions fed in to be used later for a re run of that chapter

        Args:
            qlist (list): List of questions to log
        """
        log_header_str = f'{time.localtime()} | version = {VERSION} | state = {STATE}'
        qlist.insert(0, log_header_str)
        '\n'.join(qlist)


def main():
    interface = Interface()

def test_filesystem():
    fhandler = file_handler()
    fhandler.generate_settings_file()
    print(fhandler.read_settings())
    fhandler.change_settings('pdf_file_path', 'Test val')
    print(fhandler.read_settings())

if __name__ == '__main__':
    # test_filesystem()
    main()