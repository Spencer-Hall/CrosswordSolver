# SolvingAlgorithm.py

from DataStructureCrossword import *
from english_words import get_english_words_set
from py_thesaurus import Thesaurus
import re

class Solver:

    def __init__(self, grid):
        self.grid = grid
        #self.dictionaryList = list(get_english_words_set(['web2'], lower=True))
        self.dictionaryList = ["london", "paris", "munich", "madrid", "oslo", "manchester"]

    def getCandidates(self, word):
        #return words with suitable length and common characters
        commonCharacters = {}
        for x in range(word.length):
            if word.word_cells[x].letter is not None:
                commonCharacters[x] = word.word_cells[x].letter

        correctLengthWords = [w for w in self.dictionaryList if len(w) == word.length]
        candidates = []

        for potentialWord in correctLengthWords:
            isCandidate = True

            for pos, char in commonCharacters.items():
                if char is not None and potentialWord[pos] != char:
                    isCandidate = False
                    break
            
            if isCandidate:
                candidates.append(potentialWord)

        return candidates

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

            
            
            

            
        
    