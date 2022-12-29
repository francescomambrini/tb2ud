import logging
from udapi.core.block import Block
from udapi_agldt.util.subtrees import get_subtree_depth
from tb2ud.utils import get_first_in_priority


class TransformArtificials(Block):
    ORD_LIST = ['nsubj', 'obj', 'iobj', 'obl', 'advmod', 'csubj', 'xcomp', 'ccomp', 'advcl', 'dislocated',
                'vocative', 'nmod']

    def __init__(self, with_empty=True):
        self._with_empty = with_empty
        super().__init__()

    @staticmethod
    def redraw_subtree(new_head, current_head):
        subhead = current_head.parent

        new_head.parent = subhead
        current_head.parent = new_head

        for c in current_head.children:
            if c.udeprel != 'goeswith':
                c.parent = new_head
            # and if the relation is orphaned
            if c.udeprel in TransformArtificials.ORD_LIST and c.xpos[0] in ['a', 'v', 'n', 'p']:
                c.misc['orphaned'] = 'True'


    @staticmethod
    def copy_to_empty(tree, artificial_node):
        def set_empty_ord(n, root, iteration=1):
            empty_ords = [e.ord for e in root.empty_nodes]
            neword = float(f'{n.prev_node.ord}.{iteration}')
            if neword in empty_ords:
                neword = set_empty_ord(n, root, iteration=iteration + 1)
            return neword

        lemma = artificial_node.lemma if artificial_node.lemma else None
        upos = artificial_node.upos if artificial_node.upos else None
        xpos = artificial_node.xpos if artificial_node.xpos else None
        feats = artificial_node.feats if artificial_node.feats else None
        ord_id = set_empty_ord(artificial_node, tree)
        form = f'E{ord_id}'
        empty = tree.create_empty_child(form=form, lemma=lemma, upos=upos, xpos=xpos,
                                        feats=feats)
        logging.debug(f'Creating empty node at {tree.address()} {empty.form}')

        # we set the ord now
        empty.ord = float(ord_id)

        # we also set some important misc values
        empty.misc = {'original_dep': artificial_node.misc.get('original_dep'),
                      'AposMember': artificial_node.misc.get('AposMember'),
                      'CoordMember': artificial_node.misc.get('CoordMember'),
                      'art_deps': artificial_node.misc.get('art_deps'),
                      'original_ord': str(artificial_node.misc['original_ord'])}
        return empty

    @staticmethod
    def add_deps(n, head_node, rel):
        """
        Adds a relation of the type `rel` between `n` and `head_node`, provided that:
        - the same relation is not already there
        - the node `n` is not origianlly a coordinator or a sentence adverbial
        """

        rdps = f'{head_node.ord}:{rel}'
        if rdps not in n.raw_deps and n.misc['original_dep'] not in ['AuxY', 'AuxX', 'AuxZ', 'COORD']:
            n.deps.append({'parent': head_node, 'deprel': rel})

    def process_tree(self, tree):
        subtrees = get_subtree_depth(tree)
        for subtree, depth in subtrees[::-1]:
            if subtree.misc['NodeType'] == 'Artificial':
                # original head, rel of the artificial
                original_head, original_deprel = subtree.parent, subtree.udeprel
                # make a list of the children of the artificial
                chs = subtree.children
                # in oderd to create the deps, we need children + orginal deprel
                ch_map = [(n, n.deprel) for n in chs]

                # modify deprel, which means:
                #   1. find children to promote

                newhead = get_first_in_priority(chs, self.ORD_LIST)
                if not newhead:
                    logging.error('Could not find candidates for promotion with ' +
                                  f'Artificial {subtree.address()}, {subtree.form}')
                    continue
                else:
                    # 2. redraw subtree
                    # now we know which rel should not be copied to enhanced
                    # and which rel are orphaned
                    newhead.deprel = subtree.deprel
                    self.redraw_subtree(newhead, subtree)
                    # 3. if withempty
                    if self._with_empty:
                        # 3.1 copy to empty
                        e = self.copy_to_empty(tree, subtree)
                        # 3.2 make enhanced
                        # 3.2.1 first, of the empty (if this is not aleady there!)
                        self.add_deps(e, original_head, original_deprel)
                        # 3.2.2 then, of the original children of art
                        for ch, chrel in ch_map:
                            self.add_deps(ch, e, chrel)
                    # 4. delete the useless art
                        subtree.remove(children='rehang')


