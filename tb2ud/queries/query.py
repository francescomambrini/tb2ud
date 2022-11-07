# udapy -s read.Conllu files='!*.conllu' \
#   util.Filter mark=pron keep_tree_if_node="node.upos == 'p' and node.deprel=='SBJ' and node.parent.upos=='v'" \
#   > ~/Desktop/res.conllu

from udapi.block.util.filter import Filter


class Query(Filter):
    """c
    Simple subclass of util.filter.Filter that only executes keep_tree_if_node, but accepts python functions as
    its argument
    """
    def __init__(self, func, mark=None):
        """
        :param func: a Python function that accets one argument of the type core.Node
        :param mark: string to be added to the misc column (Mark=:str)
        """
        super().__init__(mark=mark)
        self.function = func

    def process_tree(self, tree):
        root = tree

        found = False
        for node in tree.descendants:
            if self.function(node):
                found = True
                if self.mark:
                    node.misc['Mark'] = self.mark
                else:
                    return
        if not found:
            tree.remove()
        return