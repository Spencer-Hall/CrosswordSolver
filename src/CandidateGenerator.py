#CandidateGenerator.py

from DataStructureCrossword import *
from english_words import get_english_words_set
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from ast import literal_eval
import gensim.downloader as api
import pickle
import string
import requests
import inflect



class CandidateGenerator():
    def __init__(self, grid):
        self.wordvecs = self.loadWordvecs()
        if self.wordvecs == None:
            self.createFile()
            self.word_vectors = self.loadWordvecs()

        self.stopwords = stopwords.words('english') + list(string.punctuation)
        self.grid = grid
        self.solutionList = []

    def createFile(self):
        wordvecs = api.load("glove-wiki-gigaword-100")
        with open("vecs.pickle", "wb") as fp:
            pickle.dump(wordvecs, fp)

    def loadWordvecs(self):
        try:
            with open("vecs.pickle", "rb") as fp:
                wordvecs = pickle.load(fp)
            return wordvecs
        except:
            return None	
    
    def tokenise(self, clue):
        #tokenise all words in a clue, remove any stopwords with no meaning
        relevant_words = []
        for word in word_tokenize(clue.lower()):
            if word not in self.stopwords:
                relevant_words.append(word)
        return relevant_words
    
    def removeDuplicatesGensim(self, list):
        seen = set()
        new_list = []
        for x in list:
            if x[0] not in seen:
                new_list.append(x[0])
                seen.add(x[0])
        return new_list
    
    def removeDuplicates(self, list):
        seen = set()
        new_list = []
        for x in list:
            if x not in seen:
                new_list.append(x)
                seen.add(x)
        return new_list


    
    def getWikiCandidates(self, clue, length):
        request = requests.get("https://en.wikipedia.org/w/api.php?action=query&utf8=&format=json&list=search&srlimit=50&srsearch=" + clue)
        response = literal_eval(request.text)
        candidates_list = []
        
        for resp in response["query"]["search"]:
            candidate = []
            candidate = self.tokenise(resp["title"])
            for x in candidate:
                if len(x) == length:
                    candidates_list.append(x)
        
        candidates_list = self.removeDuplicates(candidates_list)

        return candidates_list


    def findSimilarWords(self, wordnet, clue, length):
        #find words most similar to the clue using most_similar()
        #allows for a smaller search space when finding similarity scored
        words = list(wordnet)
        size = 1000
        candidates = list()
        clue = clue.lower()
        
        relevant_words = self.tokenise(clue)
        
        similar = self.wordvecs.most_similar(positive=relevant_words, topn=size)
        potential_candidates = []

        for word in similar:
            if len(word[0]) == length:
                potential_candidates.append(word[0])

        #return words in both wordnet and gensim most_similar()
        candidates += list(set(words).intersection(set(potential_candidates)))

        return candidates
            
    def getSimilarities(self, clue, length):
        similar_words = self.findSimilarWords(wn.words(), clue, length)

        wordvecs = self.wordvecs

        candidates = []
        candidate_order = dict()

        relevant_words = self.tokenise(clue)
        
        inflect_engine = inflect.engine()
    
        #if the clue solution is plural or singular, as these have different lengths
        if inflect_engine.singular_noun(clue) == False: #word already singular
            inflection = "singular"
        else:
            inflection = "plural"

        for word in similar_words:
            length_of_synset = len(wn.synsets(word))

            for x in range(length_of_synset):
                tokenised = [word for word in word_tokenize(wn.synsets(word)[x].definition().lower()) if word not in self.stopwords]
                temp = word

                if len(temp) != length:
                    # Check if the plural form of the word is of same length as required by the crossword
                    if inflection == "plural" and len(inflect.plural(temp)) == length:
                        temp = inflect.plural(temp)
                    else:
                        continue

                try: 
                    #find similarity score
                    score = wordvecs.n_similarity(relevant_words, tokenised)
                except KeyError as e:
                    try:
                        #not in vocabulary error
                        delete_word = e.args[0].replace("word ", "").replace("not in vocabulary", "").replace("'", "").strip()
                        tokenised.remove(delete_word)
                        score = wordvecs.n_similarity(relevant_words, tokenised)
                    except:
                        continue
                except:
                    continue
                #this can be optimised, shows how similar word is to clue in vector space using cosine distance
                if score > 0.75:
                    try:
                        candidate_order[clue] += [(temp, score)]
                    except:
                        candidate_order[clue] = [(temp, score)]
        
        
        if(len(candidate_order) != 0):
            candidate_order = list(sorted(set(candidate_order[clue]), key=lambda x: x[1], reverse=True ))
        
        candidates = self.removeDuplicatesGensim(candidate_order)
        
        return candidates
    
    
    def getCandidates(self, word):
        #create a dictionary to return words with suitable length 
        

        #get a list of possible candidates from clue
        clue = word.clue
        wiki_candidates = self.getWikiCandidates(clue, word.length)
        gensim_candidates = self.getSimilarities(clue, word.length)
        potential_candidates = gensim_candidates + wiki_candidates
        potential_candidates = self.removeDuplicates(potential_candidates)

        #Filter candidates into those with overlapping characters

        return  potential_candidates
    

            


if __name__ == '__main__':
	
    grid = Grid()
    grid.addWord(Word(2,0,2,4,"Female King", grid)) #length 7
    word = grid.wordList[0]
    #print(CandidateGenerator(grid).getWikiCandidates(word.clue, word.length))
    print(CandidateGenerator(grid).getSimilarities(word.clue, word.length))
    #print(CandidateGenerator(grid).getCandidates(word))

    

    


