from udapi.core.block import Block


class RehangPunct(Block):
    def process_tree(self, tree):
        # TODO: code to rehang dangling punctuation in Gorman's trees correctly:
        # Gorman's trees have a series root-attached commas
        descs = tree.descendants

