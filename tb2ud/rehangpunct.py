from udapi.block.ud.fixpunct import FixPunct
import logging


class RehangPunct(FixPunct):

    def process_tree(self, tree):
        for node in tree.descendants:
            if node.misc['original_dep'] == 'AuxK' and node.parent == node.root:
                root_cands = [n for n in node.root.children if n.deprel == 'root' and n is not node]
                if len(root_cands) >= 1:
                    node.parent = root_cands[0]
                    if len(root_cands) > 1:
                        logging.warning(f'Sent {node.root.address()} has still more than 1 root!')
                else:
                    logging.error(f"Sent {node.root.address()} does not have a root!")
        super().process_tree(tree)
