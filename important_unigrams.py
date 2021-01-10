import math
import pickle
import time

import nltk

from plotting import bar_graph

start = time.time()

def idf(word, stats, document_fds):
    """Returns the inverse document frequency of a word"""
    num_docs_contains_word = sum(1 for fd in document_fds if fd[word] != 0)  # num of docs that contain the word
    return math.log(len(document_fds) / num_docs_contains_word) if word in stats else 0


# Load in unigrams
with open('data/document_fds.pickle', 'rb') as f:
    document_fds = pickle.load(f)
with open('data/unigram_fd.pickle', 'rb') as f:
    unigram_fd = pickle.load(f)

unigram_tfidf_fd = nltk.FreqDist()  # Freqdist with the number of times that a word has the top 10 tfidf position in its document

for fd in document_fds:
    # Sort by TF-IDF from high to low
    words = list(sorted(fd.keys(), key=lambda w: fd.freq(w) * idf(w, unigram_fd, document_fds), reverse=True))

    for w in words[:10]:
        unigram_tfidf_fd[w] += 1

# Update the suggestions set
with open('data/suggestions.pickle', 'rb') as f:
    suggestions = pickle.load(f)  # a set

suggestions.update({ngram: tfidf_count for ngram, tfidf_count in unigram_tfidf_fd.most_common(30)})
with open('data/suggestions.pickle', 'wb') as f:
    pickle.dump(suggestions, f)

print(f'Time elapsed: {time.time() - start}s')
bar_graph(unigram_tfidf_fd.most_common(30), 30, ['count', 'unigram'])
