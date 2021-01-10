import json
import pickle
import time

import nltk
from nltk import TrigramAssocMeasures, TrigramCollocationFinder
from nltk.corpus import stopwords

from plotting import bar_graph

start = time.time()
english_stopwords = stopwords.words('english')

# Load in unigrams
with open('data/all_words.json', 'r') as f:
    all_words = json.load(f)

def filter_pos(trigram):
    adj_noun = ('JJ', 'JJR', 'JJS', 'NN', 'NNS')  # , 'NNP', 'NNPS')
    tags = nltk.pos_tag(trigram)
    if tags[0][1] in adj_noun and tags[2][1] in adj_noun:  # the 2nd word can be anything
        return True
    return False


measures = TrigramAssocMeasures()
finder = TrigramCollocationFinder.from_words(all_words)
finder.apply_freq_filter(20)

# Mark each trigram with its PMI
stats = finder.score_ngrams(measures.pmi)
stats.sort(key=lambda g: -g[1])  # Sort by PMI from high to low

# Get top 20 trigrams that match the POS filter
pos_stats = []
i = 0

while len(pos_stats) < 20 and i < len(stats):
    if filter_pos(stats[i][0]):
        pos_stats.append(stats[i])
    i += 1

# Update the suggestions dict
with open('data/suggestions.pickle', 'rb') as f:
    suggestions = pickle.load(f)

suggestions.update({' '.join(ngram): pmi for ngram, pmi in pos_stats})
with open('data/suggestions.pickle', 'wb') as f:
    pickle.dump(suggestions, f)

print(f'Time elapsed: {time.time() - start}s')
bar_graph(pos_stats, len(pos_stats), ['pmi', 'trigram'])
