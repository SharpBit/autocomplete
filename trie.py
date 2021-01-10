# This file is basically the same thing as https://github.com/giokincade/suggest-structures/blob/master/suggesters/trie.py
# The author explained how it worked in his article and linked the code for it
# It is a trie autosuggester that is not typo-tolerant

class Node:
    """A node in the trie"""
    def __init__(self):
        self.children = {}

    def insert(self, text):
        """Adds 1 character of a string at a time"""
        if len(text) == 0:  # done adding nodes
            return
        next_char = text[0]
        # Create a node if the child character doesn't exist yet
        if not self.children.get(next_char):
            self.children[next_char] = Node()

        self.children[next_char].insert(text[1:])

    def find(self, text):
        if len(text) == 0:
            return self
        next_char = text[0]
        if self.children.get(next_char):
            return self.children[next_char].find(text[1:])
        return None

    def suggest(self, path_from_root):
        """Generator for a list of suggestions given a prefix"""
        if len(self.children) == 0:
            # No more characters
            yield path_from_root  # the suggestion itself
        for char, node in self.children.items():
            path = path_from_root + char  # add the next character as a potential suggestion
            for suggestion in node.suggest(path):
                yield suggestion


class Suggester:
    def __init__(self):
        self.root = Node()

    def add_suggestions(self, suggestions):
        for s in suggestions:
            self.root.insert(s)

    def search(self, prefix):
        # The final node of the prefix, if it exists
        node = self.root.find(prefix)
        if not node:
            return []

        return list(node.suggest(prefix))
