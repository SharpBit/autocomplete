# Autocomplete

- A simple autocompletion system that uses the Brown University corpus to generate suggestions.

### Install Dependencies
- Install Python 3.7 (add to PATH)
- Run `pip3 install -r requirements.txt` (nltk)

### Setup
1. Run `py -3 create_unigrams.py` to process the Brown University corpus.
2. Run `py -3 important_unigrams.py` add the most important unigrams to the suggestions.
3. Run `py -3 important_bigrams.py` then `py -3 important_trigrams.py` to do the same for bigrams and trigrams.
4. Run `py -3 create_trie.py` to create the trie of suggestions.
5. Run `py -3 predict_text.py` to open a tkinter window to try it out.

### How to Use
Type in something and press tab to use a suggestion. You might need to type something specific to the Brown University corpus since the variety of documents is limited.

### Example
![Example](https://i.imgur.com/10qHOhq.gif)

### Directories
- `/data` Where the processed corpus data is saved
- `/graphs` Images of the graphs created by `important_unigrams.py`, `important_bigrams.py`, and `important_trigrams.py`
