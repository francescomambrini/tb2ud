from udapi.core.block import Block


class RemoveEmpty(Block):
    def process_tree(self, tree):
        tree.empty_nodes = []

        for node in tree.descendants:
            node.raw_deps = '_'

