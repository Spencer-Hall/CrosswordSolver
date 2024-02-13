import sys
sys.path.append('/Users/spencerhall/GitRepos/CrosswordSolver/src')
from DataStructureCrossword import *
from SolvingAlgorithm import *

import csv


print("Use to test example crosswords")

selectedCrossword = input("Choose example crossword (1-3): ")

#Load file into crossword
crossword_grid = Grid()



# Open the csv file at Example Crosswords/{selectedCrossword}.csv
file_path = f"Example Crosswords/{selectedCrossword}.txt"

with open(file_path, "r") as file:
    for line in file:
        currentline = line.split(",")
        word = Word(int(currentline[0]), int(currentline[1]), int(currentline[2]), int(currentline[3]), str(currentline[4]), crossword_grid)



print("Word List:")
for word in crossword_grid.wordList:
    print(word)



#Solve crossword
print("\nSolved Grid:")
solver = Solver(crossword_grid)
solver.solve(crossword_grid, 0)
print(crossword_grid)




