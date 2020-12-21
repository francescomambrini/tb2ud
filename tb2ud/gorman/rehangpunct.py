from udapi.core.block import Block


class RehangPunct(Block):
    def process_tree(self, tree):
        # TODO: test that dangling punctuation in Gorman's trees is attached correctly:
        # Gorman's trees have a series root-attached commas
        descs = tree.descendants

