import pickle
import tkinter as tk

with open('data/suggester.pickle', 'rb') as f:
    s = pickle.load(f)

root = tk.Tk()
canvas = tk.Canvas(root, width=800, height=300)
canvas.pack()

with open('data/suggestions.pickle', 'rb') as f:
    suggestions = pickle.load(f)

# Convert tfidf counts and PMI scores into a linear scale from 0-1
unigram_divisor = max([score for ngram, score in suggestions.items() if len(ngram.split(' ')) == 1])  # ranked by tfidf count
other_ngram_divisor = max([score for ngram, score in suggestions.items() if len(ngram.split(' ')) != 1])  # ranked by PMI

def fill_text(event):
    if event.char != '\t':  # Doesn't fill unless tab is clicked
        return
    text = t.get('1.0', 'end-1c').split(' ')
    prefixes = [' '.join(text[-i:]) for i in range(1, 4) if i <= len(text)]
    all_suggestions = {}
    for pre in prefixes:
        for suggestion in s.search(pre.lower()):
            all_suggestions[suggestion] = pre
    highest_score = 0
    best_ngram = ''
    for ngram in all_suggestions.keys():
        if len(ngram.split(' ')) == 1:
            scaled = suggestions[ngram] / unigram_divisor
        else:
            scaled = suggestions[ngram] / other_ngram_divisor

        # Make suggestions like "point of view" less important if
        # "many p" is typed
        if len(all_suggestions[ngram].split(' ')) == 1:
            scaled *= 0.3

        if scaled > highest_score:
            highest_score = scaled
            best_ngram = ngram

    if best_ngram:
        t.insert('end', best_ngram[len(all_suggestions[best_ngram]):])
        t.delete(tk.END)


t = tk.Text(root, height=10, width=60, wrap='word')
t.bind('<Key>', fill_text)
t.pack()
t.focus()
canvas.create_window(400, 150, window=t)

root.mainloop()
