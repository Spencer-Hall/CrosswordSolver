# SolvingAlgorithm.py

from DataStructureCrossword import *
from english_words import get_english_words_set
import re

class Solver:

    def __init__(self, grid):
        self.grid = grid
        self.dictionaryList = list(get_english_words_set(['web2'], lower=True))

    def solve(self, grid):
        for word in grid.wordList:

            word.solve("A" * word.length)
            
            #solutionCandidates = [candidate for candidate in self.dictionaryList if len(str(candidate)) == word.length]
            #print(solutionCandidates)
            
        
    