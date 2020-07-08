import tkinter as tk
import sys
import json

# GUI window is a subclass of the basic tkinter Frame object
class HelloWorldFrame(tk.Frame):
    def __init__(self, master, content):
        # used to place labels in the window
        label_row = 0
        label_col = 0
        # Call superclass constructor
        tk.Frame.__init__(self, master)
        # Place frame into main window
        self.grid()
        # loops through every key in 'content' dictionary
        for key in content:
            # print(key, content[key])
            # print dictionary key to window
            label_key = tk.Label(self, text=f"{key}")
            label_key.grid(row=label_row, column=label_col, sticky='W')
            # print colon to window
            label_col = 1
            label_colon = tk.Label(self, text=f":")
            label_colon.grid(row=label_row, column=label_col, sticky='W')
            # print value to window
            label_col = 2
            value_string = ""
            # if the value is a list of items, create a string of all items in list
            if isinstance(content[key], list):
                separator = ", "
                value_string = separator.join(content[key])
            else:
                value_string = content[key]
            label_value = tk.Label(self, text=f"{value_string}")
            label_value.grid(row=label_row, column=label_col, sticky='W')
            # adjust label placement variables for next set of key-values
            label_row += 1
            label_col = 0

# Spawn window
if __name__ == "__main__":
    # extract commandline param that has json file name, open the file, 
    # and dump the json object into a dictionary
    player_info = json.load(open(sys.argv[1], 'r'))
    # Create main window object
    ROOT = tk.Tk()
    # Set title of window
    ROOT.title("Introduction")
    # Instantiate HelloWorldFrame object
    WELCOME_FRAME = HelloWorldFrame(ROOT, player_info)
    # Start GUI
    WELCOME_FRAME.mainloop()
