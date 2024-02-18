import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords

nltk.download('wordnet')
nltk.download('stopwords')

def filter_words(clue_tokens):
    # Get English stopwords
    stop_words = set(stopwords.words('english'))
    # Filter out stopwords and non-alphanumeric tokens
    alphanumeric_tokens = [word for word in clue_tokens if word.isalnum() and word.lower() not in stop_words]
    return alphanumeric_tokens

def tokenise(clue):
    # Tokenize clue
    clue_tokens = nltk.word_tokenize(clue)
    # Filter words
    filtered_tokens = filter_words(clue_tokens)
    return filtered_tokens

def generate_solutions(clue):
    solutions = set()
    clue_tokens = tokenise(clue)
    for token in clue_tokens:
        synsets = wordnet.synsets(token)
        for synset in synsets:
            for lemma in synset.lemmas():
                solutions.add(lemma.name().replace('_', ' '))
    return solutions


clue = "up"
potential_solutions = generate_solutions(clue)
print(potential_solutions)
