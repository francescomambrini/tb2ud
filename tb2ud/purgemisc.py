from udapi.core.block import Block


class PurgeMisc(Block):
    temp_misc = ['original_dep', 'AposMember', 'CoordMember', 'SharedMod', 'art_deps', 'original_ord', 'orphaned']

    def process_tree(self, tree):
        """
        Delete 'work-in-progress' misc attributes
        """
        nodes = tree.descendants + tree.empty_nodes
        for node in nodes:

            # first of all, if the node has misc `orphaned`,
            # then its deprel must be changed to `orphan`
            if node.misc['orphaned'] == 'True':
                node.deprel = 'orphan'

            keys = tuple(node.misc.keys())
            for k in keys:
                if k in self.temp_misc:
                    node.misc[k] = None
