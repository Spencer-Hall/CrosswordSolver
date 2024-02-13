from gensim.models import KeyedVectors
import gensim.downloader as api

#load pre-trained Word2Vec model

model = api.load("word2vec-google-news-300")

def solve_crossword(clue, top_n=5):
    # Tokenize and average word vectors for the clue
    clue_tokens = clue.lower().split()
    
    # Filter out tokens that are not present in the model vocabulary
    valid_tokens = [word for word in clue_tokens if word in model.key_to_index]

    if not valid_tokens:
        print("No valid tokens found in the model vocabulary.")
        return []

    clue_vector = sum(model.get_vector(word) for word in valid_tokens) / len(valid_tokens)

    # Find words in the vocabulary most similar to the clue vector
    similar_words = model.similar_by_vector(clue_vector, topn=top_n)

    return similar_words

# Example usage
clue = "Capital of France"

result = solve_crossword(clue)
print("Top matching words:")
for word, similarity in result:
    print(f"{word}: {similarity}")
