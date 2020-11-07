from udapi.core.block import Block


class RemoveArts(Block):
    """
    An Artificial Node that does not govern anything is a useless node.
    It can be safely removed.
    """
    def process_node(self, node):
        chs = node.children
        if node.misc['NodeType'] == 'Artificial' and not chs:
            # delete! The `warn` argument should be useless, but better safe than sorry...
            node.remove(children="warn")
