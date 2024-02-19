# SolvingAlgorithm.py


from DataStructureCrossword import *
from CandidateGenerator import *
from english_words import get_english_words_set
from py_thesaurus import Thesaurus
import re

from nltk.corpus import wordnet 

class Solver:

    def __init__(self, grid):
        self.grid = grid
        self.solutionList = []

    def getCandidates(self, word):
        
        candidateGenerator = CandidateGenerator(self.grid)
        return candidateGenerator.getCandidates(word)

    #Backtracking approach to solve the grid
    def solve(self, grid, index):
        if index == len(grid.wordList):
            #all words are solved, the puzzle is complete
            return grid

        word = grid.wordList[index]
        candidates = self.getCandidates(word)

        for candidate in candidates:
            self.applyCandidate(word, candidate)

            #recursively try to solve the next word
            result = self.solve(grid, index + 1)
            if result is not None:
                return result  # Found a solution

            #if the current candidate did not lead to a solution, undo the changes
            self.undoCandidate(word)

        #no solution found 
        return None

    def applyCandidate(self, word, candidate):
        word.solve(candidate)
                    
    def undoCandidate(self, word):
        word.isSolved = False
        word.solution = None
        for cell in word.word_cells:
            cell.solve(None)

            
            
            

            
        
    