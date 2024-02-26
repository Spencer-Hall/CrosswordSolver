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
        self.candidates = {}
        self.candidateGenerator = CandidateGenerator(self.grid)

    def generateCandidates(self, word):
        candidate_list = self.candidateGenerator.getCandidates(word)
        self.candidates.update({word.clue: candidate_list})

    def getCandidates(self, word):
        return self.candidates[word.clue]

    #Backtracking approach to solve the grid
    def solve(self):
        for word in self.grid.wordList:
            self.generateCandidates(word)
        return self.backtrackSolve(self.grid, 0)
    
    def backtrackSolve(self,grid,index):
        if index == len(grid.wordList):
            #all words are solved, the puzzle is complete
            return grid

        word = grid.wordList[index]
        candidates = self.getCandidates(word)

        for candidate in candidates:
            if(self.applyCandidate(word, candidate)):

                #recursively try to solve the next word
                result = self.backtrackSolve(grid, index + 1)
                if result is not None:
                    return result  # Found a solution

                #if the current candidate did not lead to a solution, undo the changes
                self.undoCandidate(word)

        #no solution found 
        return None


    def applyCandidate(self, word, candidate):
        commonCharacters = {}
        for x in range(word.length):
            if word.word_cells[x].letter is not None:
                commonCharacters[x] = word.word_cells[x].letter

        isCandidate = True

        for pos, char in commonCharacters.items():
            if char is not None and candidate[pos] != char:
                isCandidate = False
                break

        if isCandidate:
            word.solve(candidate)
            return True
        else:
            return False


                    
    def undoCandidate(self, word):
        word.isSolved = False
        word.solution = None
        for cell in word.word_cells:
            cell.solve(None)

            
            

            
        
    