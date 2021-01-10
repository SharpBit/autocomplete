import json
import pickle
import time

import nltk
from nltk import BigramAssocMeasures, BigramCollocationFinder
from nltk.corpus import stopwords

from plotting import bar_graph

start = time.time()
english_stopwords = stopwords.words('english')

# Load in unigrams
with open('data/all_words.json', 'r') as f:
    all_words = json.load(f)

def filter_pos(bigram):
    adj_noun = ('JJ', 'JJR', 'JJS', 'NN', 'NNS')  # , 'NNP', 'NNPS')
    noun = ('NN', 'NNS')  # , 'NNP', 'NNPS')
    titled = []
    for w in bigram:
        if w in english_stopwords:
            return False
        titled.append(w.title())
    tags = nltk.pos_tag(bigram)
    title_tags = nltk.pos_tag(tuple(titled))  # To eliminate proper nouns from overfilling the top 20
    if tags[0][1] in adj_noun and tags[1][1] in noun:
        if not (title_tags[0][1].endswith('P') or title_tags[1][1].endswith('P')):
            return True
    return False


measures = BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(all_words)
finder.apply_freq_filter(20)


# Mark each bigram with its PMI
stats = finder.score_ngrams(measures.pmi)
stats.sort(key=lambda g: -g[1])  # Sort by PMI from high to low

# Get top 20 bigrams that match the POS filter
pos_stats = []
i = 0
while len(pos_stats) < 50 and i < len(stats):
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
bar_graph(pos_stats[:20], 20, ['pmi', 'bigram'])
