from tkinter import Tk, BOTH, Canvas
import time # part of optional pause in self.wait_for_close() loop

class Window:
    def __init__(self, width, height):
        if width <= 0 or height <= 0:
            raise ValueError(f"Window parameters out of bounds: width={width}, height={height}")
        
        self.width = width
        self.height = height

        self.root = Tk() # can change to self.__root for more privacy for root
        """
         Creates an instance of the Tk class, which initializes Tk and creates its associated Tcl interpreter.
         It also creates a toplevel window, known as the root window, which serves as the main window of the application.
         """
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.root.title("Maze Solver") 

        bg_color = 'grey' #arbitrary for now

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
        if x < 0 or y < 0:
            raise ValueError(f"Point out of bounds: x={x}, y={y}")
        
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
        
class Cell:
    def __init__(self, top_left_point, bottom_right_point, win = None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.x1 = top_left_point.x
        self.y1 = top_left_point.y
        self.x2 = bottom_right_point.x
        self.y2 = bottom_right_point.y
        self.win = win

    def draw(self, fill_color=None):
        if self.win is None:
            return
        
        if fill_color is None:
            fill_color = "black" # default if no color specified

        walls = {
            "left": (self.x1, self.y1, self.x1, self.y2, self.has_left_wall),
            "right": (self.x2, self.y1, self.x2, self.y2, self.has_right_wall),
            "top": (self.x1, self.y1, self.x2, self.y1, self.has_top_wall),
            "bottom": (self.x1, self.y2, self.x2, self.y2, self.has_bottom_wall),
        }

        for wall, (x1, y1, x2, y2, has_wall) in walls.items():
            # Erase (or redraw with "grey") if wall is missing
            color = "black" if has_wall else "grey"
            point_a = Point(x1, y1)
            point_b = Point(x2, y2)
            wall_line = Line(point_a, point_b)
            wall_line.draw(self.win, color)

        """
        # old implimentation
        if self.has_left_wall:
            point_a = Point(self.x1, self.y1)
            point_b = Point(self.x1, self.y2)
            left_wall = Line(point_a, point_b)
            left_wall.draw(self.win, fill_color)

        if self.has_right_wall:
            point_a = Point(self.x2, self.y1)
            point_b = Point(self.x2, self.y2)
            right_wall = Line(point_a, point_b)
            right_wall.draw(self.win, fill_color)

        if self.has_top_wall:
            point_a = Point(self.x1, self.y1)
            point_b = Point(self.x2, self.y1)
            top_wall = Line(point_a, point_b)
            top_wall.draw(self.win, fill_color)

        if self.has_bottom_wall:
            point_a = Point(self.x1, self.y2)
            point_b = Point(self.x2, self.y2)
            bottom_wall = Line(point_a, point_b)
            bottom_wall.draw(self.win, fill_color)
        """

    def draw_move(self, to_cell, undo=False):
        fill_color = "red"
        if undo:
            fill_color = "grey" # default if no color specified

        point_1 = Point(((self.x1+self.x2)/2), ((self.y1 + self.y2)/2))
        point_2 = Point(((to_cell.x1+to_cell.x2)/2), ((to_cell.y1 + to_cell.y2)/2))
        move_line = Line(point_1, point_2)
        move_line.draw(self.win, fill_color)

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None):
        if x1 < 0 or y1 < 0:
            raise ValueError(f"Maze offset out of bounds: x1={x1}, y1={y1}")
        if num_rows <= 0 or num_cols <= 0:
            raise ValueError(f"Maze dimensions out of bounds: num_rows={num_rows}, num_cols={num_cols}")
        if cell_size_x <= 0 or cell_size_y <= 0:
            raise ValueError(f"Maze cell sizes out of bounds: cell_size_x={cell_size_x}, cell_size_y={cell_size_y}")
        
        
        self.x1 = x1 # x1 and y1 here are offsets for the grid, shifting the top left starting point.
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        self._create_cells()

    def _create_cells(self):
        # access with self._cells[col]prow]  (col is x, row is y)

        self._cells = []

        for col in range(self.num_cols):
            column = [] # new list for this column

            for row in range(self.num_rows): #self.x1 and y1 are the offsets x = cols, y = rows
                new_cell_x1 = self.x1 + col * self.cell_size_x
                new_cell_y1 = self.y1 + row * self.cell_size_y
                new_cell_x2 = new_cell_x1 + self.cell_size_x
                new_cell_y2 = new_cell_y1 + self.cell_size_y

                new_point_1 = Point(new_cell_x1, new_cell_y1)
                new_point_2 = Point(new_cell_x2, new_cell_y2)

                new_cell = Cell(new_point_1, new_point_2, self.win)
                new_cell.draw()
                column.append(new_cell)

            self._cells.append(column)
        self._break_entrance_and_exit()
        
    def _draw_cell(self, i, j): # i, j are col, row (x, y) coordinates for the self_Cells matrix
        self._cells[i][j].draw()
        self._animate()

    def _animate(self):
        self.win.update()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self.num_cols - 1][self.num_rows-1].has_bottom_wall = False
        self._draw_cell(self.num_cols-1, self.num_rows-1)



def main():
    win = Window(420, 420)
    """
    point1 = Point(10, 100)
    point2 = Point(50, 200)
    line = Line(point1, point2)
    color = "red"
    win.draw_line(line, color)

    cell_one = Cell(point1, point2, win.canvas)
    cell_one.draw()

    point1.x = 0
    point1.y = 0
    point2.x = 150
    point2.y = 400

    cell_two = Cell(point1, point2, win.canvas)
    #cell_two.has_bottom_wall = False
    #cell_two.has_top_wall = False
    #cell_two.has_left_wall = False
    #cell_two.has_right_wall= False

    cell_two.draw()

    cell_one.draw_move(cell_two)
    cell_one.draw_move(cell_two, True)
    """
    my_maze = Maze(10, 10, 20, 20, 20, 20, win.canvas)
    
    
    """
    # Below is just a silly "animation", not in the assignment

    a = 1
    b = 200
    c = 0
    temp = 1
    step = 1
    while temp < 10:
        print(f"a: {a}, b: {b}, step: {step}")
        for i in range(a, b, step):
            point1.x = i + 1
            point1.y = 2*i + 1
            point2.x = 2*i + 1
            point2.y = i + 1
            line = Line(point1, point2)
            if i % 2 == 0:
                color = "red"
            else:
                color = "black" 

            win.draw_line(line, color)
            win.root.update()  # Add this!
            time.sleep(0.01)
            win.canvas.delete("all")  # Clear for next frame
            

        a, b = b, a
        step = step * -1
        
        
        
        temp += 1
    """
                        
    win.wait_for_close()


main()