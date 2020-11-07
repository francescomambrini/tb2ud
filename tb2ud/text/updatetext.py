from udapi.core.block import Block


class UpdateText(Block):

    def process_tree(self, tree):
        txt = tree.compute_text()
        tree.text = txt
