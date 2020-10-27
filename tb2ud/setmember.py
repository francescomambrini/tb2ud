from udapi.core.block import Block

class SetMember(Block):

    def process_node(self, node):
        if "_AP" in node.deprel:
            node.misc['AposMember'] = True
        if "_CO" in node.deprel:
            node.misc['CoordMember'] = True
