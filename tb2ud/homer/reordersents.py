"""
Reorders the sentences in the Homeric treebank. The problem is that the tb sentences
were ordered based on the canonical ref _as strings_ (thus 1.10 precedes 1.2). Although
it is not necessarily a problem, it is inconvenient for human readability.
"""

from udapi.core.block import Block

class ReorderSents(Block):
    def process_tree(self, tree):
        pass