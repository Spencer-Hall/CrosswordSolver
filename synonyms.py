# synonyms.py


from nltk.corpus import wordnet 


    

#get synonyms
clue = input("Enter word")
synonyms = []
for syn in wordnet.synsets(clue): 
    for l in syn.lemmas(): 
        synonyms.append(l.name()) 

print(synonyms)


      
            
            
            

            
        
    