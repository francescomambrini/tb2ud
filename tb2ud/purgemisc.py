from udapi.core.block import Block


class PurgeMisc(Block):
    temp_misc = ['original_dep', 'AposMember', 'CoordMember']

    def process_node(self, node):
        """
        Delete 'work-in-progress' misc attributes
        """
        keys = tuple(node.misc.keys())
        for k in keys:
            if k in self.temp_misc:
                node.misc[k] = None
