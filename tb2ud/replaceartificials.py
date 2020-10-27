from udapi.core.block import Block
import logging

# DEPRECATED! Seems useless


class ReplaceArtificials(Block):
    def __init__(self, insert_enhanced=False):
        """

        Parameters
        ----------
        insert_enhanced (bool):
            if True, insert a reconstructed node for enhanced dependencies
        """

        self._enhanced = bool(insert_enhanced)
        super(ReplaceArtificials, self).__init__()

    def process_node(self, node):
        if node.misc['NodeType'] == 'Artificial':
            parent = node.parent
            chs = node.children
            # seek for a node to promote
            # 1 if there are prepositions like ἔπι or πάρα, we promote them
            pass


