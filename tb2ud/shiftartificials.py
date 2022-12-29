from udapi.core.block import Block
from udapi_agldt.util.subtrees import get_subtree_depth


class ShiftArtificials(Block):

    def process_tree(self, tree):
        """
        Shift the order of the artificials before you redraw the subtree. Useful, if you plan to include
        the empty nodes and deps for the artificial nodes
        """
        subtrees = get_subtree_depth(tree)
        for n, _ in subtrees:
            if n.misc['NodeType'] == 'Artificial':
                n.shift_before_subtree(n, without_children=True)
