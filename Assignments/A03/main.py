import tkinter as tk

# GUI window is a subclass of the basic tkinter Frame object
class HelloWorldFrame(tk.Frame):
    def __init__(self, master, name):
        # Call superclass constructor
        tk.Frame.__init__(self, master)
        # Place frame into main window
        self.grid()
        # Create text box with "Hello World" text
        hello = tk.Label(self, text=f"Hello World! My name is {name}!")
        # Place text box into frame
        hello.grid(row=0, column=0)

# Spawn window
if __name__ == "__main__":
    # Create main window object
    ROOT = tk.Tk()
    # Set title of window
    ROOT.title("Hello World!")
    # Instantiate HelloWorldFrame object
    HELLO_FRAME = HelloWorldFrame(ROOT, "Corbin Matamoros")
    # Start GUI
    HELLO_FRAME.mainloop()
    