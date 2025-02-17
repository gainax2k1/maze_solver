from tkinter import Tk, BOTH, Canvas
import time # part of optional pause in self.wait_for_close() loop

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.root = Tk() # can change to self.__root for more privacy for root
        """
         Creates an instance of the Tk class, which initializes Tk and creates its associated Tcl interpreter.
         It also creates a toplevel window, known as the root window, which serves as the main window of the application.
         """
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.root.title("Maze Solver") 

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
            time.sleep(0.01)  # Adds a slight pause to reduce CPU usage, optional

    def close(self):
        self.running = False

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.x = x # x=0 left of screen  # public becauses not self.__x and self.__y
        self.y = y # y=0 top of screen


class Line:
    def __init__(self, point_a, point_b):
        self.point_a = point_a
        self.point_b = point_b

    def draw(self, canvas, fill_color): # Canvas?
        x1 = self.point_a.x
        y1 = self.point_a.y
        x2 = self.point_b.x
        y2 = self.point_b.y
        canvas.create_line(x1, y1, x2, y2, fill = fill_color, width = 2)
        


def main():
    win = Window(800, 600)
    point1 = Point(10, 100)
    point2 = Point(50, 200)
    line = Line(point1, point2)
    win.draw_line(line, "red")

    win.wait_for_close()


main()