import json
import pickle
import time

import nltk
from nltk.corpus import brown, stopwords

start = time.time()
document_fds = []
english_stopwords = stopwords.words('english')
tfidf_fd = nltk.FreqDist()
all_words = [w.lower() for w in brown.words() if w.isalpha() and w.lower() != 'af']
all_nouns = []

# Filter words to make sure they have the characters [A-z] and are not a stopword
for i, fileid in enumerate(brown.fileids()):
    # Af is often used to replace equations and formulas and sways the importance of the word
    filtered_words = [w.lower() for w in brown.words(fileid) if w.isalpha() and w.lower() not in english_stopwords and w.lower() != 'af']
    # Filter out certain parts of speech
    tagged_words = nltk.pos_tag(filtered_words)
    tagged_filtered_words = [word for word, pos in tagged_words if pos.startswith('NN')]
    all_nouns += tagged_filtered_words
    doc_fd = nltk.FreqDist(tagged_filtered_words)
    document_fds.append(doc_fd)

with open('data/document_fds.pickle', 'wb') as f:
    pickle.dump(document_fds, f)

unigram_fd = nltk.FreqDist(all_nouns)
with open('data/unigram_fd.pickle', 'wb') as f:
    pickle.dump(unigram_fd, f)

with open('data/all_words.json', 'w') as f:
    json.dump(all_words, f)

with open('data/all_nouns.json', 'w') as f:
    json.dump(all_nouns, f)

# Set up the suggestions set for the other programs
with open('data/suggestions.pickle', 'wb') as f:
    pickle.dump(dict(), f)

print(f'Time elapsed: {time.time() - start}s')
