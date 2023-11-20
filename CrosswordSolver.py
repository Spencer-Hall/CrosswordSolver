# CrosswordSolver.py

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from DataStructureCrossword import *
from SolvingAlgorithm import *


import sys

class CluesWidget(QWidget):
    def __init__(self, grid):
        super().__init__()
        self.grid = grid

        layout = QVBoxLayout()

        title_label = QLabel("CLUES")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        self.vertCount = 0
        self.horiCount = 0

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)  

        self.solve_button = QPushButton("SOLVE")
        self.solve_button.clicked.connect(self.solvePuzzle)


        layout.addWidget(self.text_edit)
        layout.addWidget(self.solve_button)
         
        self.setLayout(layout)

        size_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setSizePolicy(size_policy)

    def addClue(self, clue, orientation):
        if(orientation == 0):
            self.text_edit.append(f"{self.vertCount} DOWN: {clue}")
            self.vertCount += 1
        else:
            self.text_edit.append(f"{self.horiCount} ACROSS: {clue}")
            self.horiCount += 1

    def solvePuzzle(self):
        print("SOLUTIONS")
        solver = Solver(self.grid)
        solver.solve(self.grid, 0)
        print(self.grid)
        



class CrosswordGrid(QWidget):
    def __init__(self, rows, columns, grid, clues):
        super().__init__()
        self.rows = rows
        self.columns = columns
        self.grid = grid
        self.clues = clues
        self.cell_width = 35
        self.cell_height = 35
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)
        self.setLayout(grid_layout)

        # Create the grid of QLabel widgets
        self.cells = [[QLabel() for _ in range(columns)] for _ in range(rows)]
        self.dragging = False
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

        # Add cells to the grid layout
        for row in range(rows):
            for col in range(columns):
                cell = self.cells[row][col]
                cell.setFixedSize(35, 35)
                cell.setContentsMargins(0, 0, 0, 0)
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center text in each cell
                cell.setStyleSheet("border: 0.5px solid gray; padding: 0px; margin: 0px;")  # Add border style
                grid_layout.addWidget(cell, row, col)
                grid_layout.setContentsMargins(0,0,0,0)
                grid_layout.setSpacing(0)


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Calculate the grid cell clicked based on the mouse event
            x = (event.pos().x() - 12) // (self.cell_width + 10)
            y = (event.pos().y() - 12) // (self.cell_height + 8)

            # Start dragging from this cell
            self.start_x = x
            self.start_y = y
            self.end_x = x
            self.end_y = y
            self.dragging = True

            
        
    def mouseMoveEvent(self, event):
        if self.dragging:
            # Calculate the current cell based on the mouse event
            x = (event.pos().x() - 12) // (self.cell_width + 10)
            y = (event.pos().y() - 12) // (self.cell_height + 8)

            # Update the end position as the user drags
            self.end_x = x
            self.end_y = y

    
        
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Stop dragging
            self.dragging = False
            # Process the user's input (start and end positions)
            
            start_x = self.start_y
            start_y = self.start_x
            end_x = self.end_y
            end_y = self.end_x


            if (start_x == end_x and end_y >= start_y):
                orientation = 1 #down
            elif (start_y == end_y and end_x >= start_x):
                orientation = 0 #across
            else:
                print("ERROR")
                exit
            
            #Check if coords valid 
            
            print(f"User input: Start: ({start_x}, {start_y}), End: ({end_x}, {end_y})")
            #check if word overlaps another
            #If valid, ask for clue input 
            clue, ok = QInputDialog().getText(self, "Clue Entry", "Clue: ")
            
            if ok == False: 
                print("ERROR")
                exit
            #Create word 
            word = Word(start_x, start_y, end_x, end_y, clue, self.grid)

            #Add clue to clue widget
            self.clues.addClue(clue, orientation)

            #shade 
            if start_x == end_x:
                for y in range (start_y, end_y + 1):
                    cell = self.cells[start_x][y]
                    cell.setStyleSheet("border: 0.5px solid gray; padding: 0px; margin: 0px; background-color: grey")
            else:
                for x in range (start_x, end_x + 1):
                    cell = self.cells[x][start_y]
                    cell.setStyleSheet("border: 0.5px solid gray; padding: 0px; margin: 0px; background-color: grey")

            
            
            
                       
    


class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Crossword Solver")
        self.setFixedSize(1100,700)

        newGrid = Grid()
        self.clues_widget = CluesWidget(newGrid)
        self.grid = CrosswordGrid(15, 15, newGrid, self.clues_widget)
        

        # Create a horizontal layout for the main window
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.grid)
        main_layout.addWidget(self.clues_widget)

        self.clues_widget.setFixedWidth(350)

        # Create a central widget for the main window and set the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        


        




app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()


