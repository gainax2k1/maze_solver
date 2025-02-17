from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.root = Tk() 
        """
         Creates an instance of the Tk class, which initializes Tk and creates its associated Tcl interpreter.
         It also creates a toplevel window, known as the root window, which serves as the main window of the application.
         """
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.root.title("Maze Solver") #not sure if write method?
        # ttk.Label(frm, text="Hello World!").grid(column=0, row=0)   #potential alternative title method?


        bg_color = 'gray75' #arbitrary for now

        self.canvas = Canvas(self.root, width=self.width, height=self.height, background=bg_color) 

        self.canvas.pack() # Pack the Canvas widget

        self.running = False


    def redraw(self): #  Redraws all the graphics in the window.
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.running = True

        while self.running:
            self.redraw()
        
    def close(self):
        self.running = False

def main():
    win = Window(800, 600)
    win.wait_for_close()


main()