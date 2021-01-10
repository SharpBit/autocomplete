import pickle

from trie import Suggester

with open('data/suggestions.pickle', 'rb') as f:
    suggestions = list(pickle.load(f))

s = Suggester()
s.add_suggestions(suggestions)
with open('data/suggester.pickle', 'wb') as f:
    pickle.dump(s, f)
