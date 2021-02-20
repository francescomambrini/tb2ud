from udapi.core.block import Block
from udapi.block.agldt.agldt_util.subtrees import get_subtree_depth
from tb2ud.utils import get_first_in_priority



class TransformArtificials(Block):

    def __init__(self, with_empty=True):
        self._with_empty = with_empty
        super().__init__()

    def process_tree(self, tree):
        subtrees = get_subtree_depth(tree)
        for subtree in subtrees[::-1]:
            if subtree.misc['NodeType'] == 'Artificial':
                pass
                # modify deprel, which means:
                #   1. find children to promote
                #   2. assign correct label
