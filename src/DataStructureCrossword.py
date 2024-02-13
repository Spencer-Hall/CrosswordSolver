# DataStructureCrossword.py


#CharCell represents an individual cell in the crossword grid
# Given co-ordinates x,y a boolean isSolved and a letter initialised to None
class CharCell:
    def __init__(self, x, y, isSolved=False, letter=None):
        self.x = x
        self.y = y
        self.isSolved = isSolved
        self.letter = letter

    def set_letter(self, letter):
        if not self.isSolved:
            self.letter = letter

    def solve(self, letter):
        self.isSolved = True
        self.letter = letter

    def get_solved(self):
        if(self.isSolved):
            return self.letter
        return False
    
    def __str__(self):
        return f"({self.x}, {self.y}) Solved: {self.isSolved}, Letter: {self.letter}"
    

#Grid represents the crossword grid, built with a 2D 15x15 array of CharCells.
#Contains an array wordList, which is where the words added to the grid will be stored.     
class Grid:
    def __init__(self):
        self.rows = 15
        self.columns = 15
        self.wordList = []
        self.isSolved = False
        self.grid = [[CharCell(x, y) for y in range(self.columns)] for x in range(self.rows)]

    def addWord(self, word):
        self.wordList.append(word)

    def get_cell(self, x, y):
        if 0 <= x < self.rows and 0 <= y < self.columns:
            return self.grid[x][y]
        return None

    def __str__(self):
        grid_str = ""
        for row in self.grid:
            row_str = " ".join(f"{cell.letter or '.'}" for cell in row)
            grid_str += row_str + "\n"
        return grid_str

#Word represents a place on the grid where a word should be placed given solutions
#Given start and end co-ordinates, an associated clue, boolean isSolved and a solution
class Word:
    def __init__(self, start_x, start_y, end_x, end_y, clue, grid, isSolved=False, solution=None, word_name=None):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.word_cells = []
        self.clue = clue
        self.isSolved = isSolved
        self.solution = solution
        self.word_name = word_name
        self.grid = grid
        self.grid.addWord(self)
        self.orientation = None
        self.length = 0
        
        if start_x == end_x and end_y >= start_y: #Horizontal word
            self.orientation = 0
            for y in range(start_y, end_y + 1):
                cell = grid.get_cell(start_x, y)
                self.word_cells.append(cell)
                self.length +=1  
        elif start_y == end_y and end_x >= start_x: #Vertical word
            self.orientation = 1
            for x in range(start_x, end_x + 1):
                cell = grid.get_cell(x, start_y)
                self.word_cells.append(cell)
                self.length +=1
        else: #Invalid word
            return False


    def solve(self, solution):
        if len(solution) == len(self.word_cells):
            for x in range(len(solution)):
                self.word_cells[x].solve(solution[x])   
            self.isSolved = True
            self.solution = solution

    def __str__(self):
        return f"Word: {self.word_name}\nStart: ({self.start_x}, {self.start_y})\nEnd: ({self.end_x}, {self.end_y})\nClue: {self.clue}\nSolved: {self.isSolved}\nSolution: {self.solution}\nWord Cells: {self.word_cells}"
    


    


    


