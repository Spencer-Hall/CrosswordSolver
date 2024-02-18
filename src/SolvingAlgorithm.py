# SolvingAlgorithm.py

#Filter clue by removing stop words, give antonyms if required

#Separate solver using chatgpt?
#Seperate solver using generated dictionary?

from DataStructureCrossword import *
from english_words import get_english_words_set
from py_thesaurus import Thesaurus
import re

from nltk.corpus import wordnet 

class Solver:

    def __init__(self, grid):
        self.grid = grid
        self.solutionList = []

    def getCandidates(self, word):
        #return words with suitable length and common characters
        commonCharacters = {}
        for x in range(word.length):
            if word.word_cells[x].letter is not None:
                commonCharacters[x] = word.word_cells[x].letter

        #get synonyms
        clue = word.clue
        synonyms = []
        for syn in wordnet.synsets(clue): 
            for l in syn.lemmas(): 
                synonyms.append(l.name()) 

    

        correctLengthWords = [w for w in synonyms if len(w) == word.length]
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

            
            
            

            
        
    