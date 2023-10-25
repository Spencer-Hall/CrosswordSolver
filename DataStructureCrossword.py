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
        return f"({self.x}, {self.y}) - Shared: {self.isSharedCell}, Solved: {self.isSolved}, Letter: {self.letter}"
    
class Grid:
    def __init__(self):
        self.rows = 15
        self.columns = 15
        self.grid = [[CharCell(x, y) for y in range(self.columns)] for x in range(self.rows)]

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
        #TODO Initialise word_cells as list of CharCells in given direction
        if start_x == end_x and end_y >= start_y: #Horizontal word
            for y in range(start_y, end_y + 1):
                cell = grid.get_cell(start_x, y)
                cell.set_letter("□")
                self.word_cells.append(cell)  
        elif start_y == end_y and end_x >= start_x: #Vertical word
            for x in range(start_x, end_x + 1):
                cell = grid.get_cell(x, start_y)
                cell.set_letter("□")
                self.word_cells.append(cell)
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
    

# Example usage
if __name__ == "__main__":
    # Create a grid
    crossword_grid = Grid()

    #Assign a word to the grid
    word1 = Word(2, 1, 2, 5, "Clue", crossword_grid)
    word2 = Word(2, 1, 6, 1, "Clue", crossword_grid)
    word3 = Word(4, 4, 7, 4, "Clue", crossword_grid)
    word4 = Word(6, 1, 6, 7, "Clue", crossword_grid)
    word5 = Word(8, 7, 8, 14, "Clue", crossword_grid)
    word6 = Word(9, 3, 9, 7, "Clue", crossword_grid)
    word7 = Word(8, 7, 14, 7, "Clue", crossword_grid)
    word8 = Word(14, 1, 14, 6, "Clue", crossword_grid)
    #word.solve("spoon")

    # Print the grid
    print(crossword_grid)


