from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *



import sys

class CrosswordGrid(QWidget):
    def __init__(self, rows, columns):
        super().__init__()
        self.rows = rows
        self.columns = columns
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
            x = event.pos().x() // self.cell_width
            y = event.pos().y() // self.cell_height

            # Start dragging from this cell
            self.start_x = x
            self.start_y = y
            self.end_x = x
            self.end_y = y
            self.dragging = True
        
    def mouseMoveEvent(self, event):
        if self.dragging:
            # Calculate the current cell based on the mouse event
            x = event.pos().x() // (self.cell_width + 12)
            y = event.pos().y() // (self.cell_height + 12)

            # Update the end position as the user drags
            self.end_x = x
            self.end_y = y
        
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Stop dragging
            self.dragging = False

            # Process the user's input (start and end positions)
            print(f"User input: Start: ({self.start_x}, {self.start_y}), End: ({self.end_x}, {self.end_y})")


class CluesWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        title_label = QLabel("CLUES")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)


        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)  

        self.solve_button = QPushButton("SOLVE")
        #self.solve_button.clicked.connect(self.solve_puzzle)


        layout.addWidget(self.text_edit)
        layout.addWidget(self.solve_button)
         
        self.setLayout(layout)

        size_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setSizePolicy(size_policy)

class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Crossword Solver")
        self.setFixedSize(1100,700)

        self.grid = CrosswordGrid(15, 15)
        self.clues_widget = CluesWidget()

        # Create a horizontal layout for the main window
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.grid)
        main_layout.addWidget(self.clues_widget)

        self.clues_widget.setFixedWidth(350)

        # Create a central widget for the main window and set the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.clues_widget.text_edit.setPlainText("Across Clues:\n1. A type of fruit\n2. A four-legged animal\n\nDown Clues:\n1. A liquid that falls from the sky\n2. The opposite of up")


        




app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()


