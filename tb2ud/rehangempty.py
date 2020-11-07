from udapi.core.block import Block
import logging


class RehangEmpty(Block):
    def process_tree(self, tree):
        # TODO: code to redefine the position of the Empty Nodes
        empties = tree.empty_nodes
        try:
            root = [c for c in tree.children if c.deprel == 'root'][0]
        except IndexError:
            logging.error(f'Sentence {tree.address()} has no root?')
        else:
            for empty in empties:
                empty.deps.append({'parent': original_head, 'deprel': subtree.deprel})

