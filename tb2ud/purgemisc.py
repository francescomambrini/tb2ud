from udapi.core.block import Block


class PurgeMisc(Block):
    temp_misc = ['original_dep', 'AposMember', 'CoordMember', 'art_deps', 'original_ord']

    def process_tree(self, tree):
        """
        Delete 'work-in-progress' misc attributes
        """
        nodes = tree.descendants + tree.empty_nodes
        for node in nodes:
            keys = tuple(node.misc.keys())
            for k in keys:
                if k in self.temp_misc:
                    node.misc[k] = None
