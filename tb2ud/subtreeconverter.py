import logging

from udapi.core.block import Block
from udapi.block.agldt.agldt_util.subtrees import get_subtree_depth
from tb2ud.utils.constructions import *
from tb2ud.utils import get_first_in_priority


class SubTreeConverter(Block):
    """
    Convert AGLDT-style trees to UD by re-designing the tree structure when
    necessary (e.g. coordination, preposition/conjunction, ellipsis, copula...).

    It expects that some shallow conversion has already been performed, e.g. by
    running the `ShallowConverter` in the `shallowconverter.py` and that the original
    deprel label are stored in a misc value field. Thus, in any pipeline, it's
    best to pipe this module after the `ShallowConverter`.

    It works bottom-up, ordering the structures in each trees using
    `the get_subtree_depth` function defined in `udapi.block.agldt.agldt_util.subtrees`.
    This function sorts the subtrees bottom-up, i.e. from the lowest depth up to
    the children of the sentence root. A subtree is nothing more than a non-leaf
    node in the dependency tree. Only the subtree-root (i.e. the non-leaf node)
    is returned; children and descendants can be easily obtained using the
    `Node` methods and attributes.

    The advantage of working bottom-up is that we don't need to worry about situations
    like AuxP governing two coordinated nouns. When the transformation reaches
    the root of the prepositional phrase (the AuxP-node), the coordination at the
    lower level has already been taken care of and appropriately converted.

    """

    def __init__(self, with_enhanced=False):
        """
        Rehang constructions and either preserves the artificial nodes with enhanced deps or not

        Parameters
        ----------
        with_enhanced : bool
            if true, artificial nodes are introduced and their dependencies are recorded in the enhanced deps
            (default=False)

        """
        self._with_enhanced = with_enhanced
        super().__init__()

    @staticmethod
    def redraw_subtree(new_head, current_head):
        subhead = current_head.parent

        new_head.parent = subhead
        current_head.parent = new_head

        # if there are interesting misc values on the old head, pass them to the new one!
        # but don't blank it, if the current head is no member
        if current_head.misc['AposMember']:
            new_head.misc['AposMember'] = current_head.misc['AposMember']
        if current_head.misc['CoordMember']:
            new_head.misc['CoordMember'] = current_head.misc['CoordMember']

        for c in current_head.children:
            if c.udeprel != 'goeswith':
                c.parent = new_head

    @staticmethod
    def attach_right(element, attr, val):
        """
        Re-attach the node `element` to the the first sibling on the right whose attribute `attr` matches `val`

        Parameters
        ----------
        element : udapi.core.node.Node
            the node to reattach to the first right sibling
        attr : str
            the attribute of node to be checked (e.g. `udeprel`)
        val : str
            the value to be matched; must be a valid value for that `atr` (e.g. `conj`)
        """
        h = element.parent
        right_bros = [ch for ch in h.children if ch.precedes(element) is False]
        for b in right_bros:
            checked_val = getattr(b, attr)
            if checked_val == val:
                element.parent = b
                return None

    def process_tree(self, tree):
        subtrees = get_subtree_depth(tree)

        # the logic that goes here: we have to consider the type of relation
        # between this subtree and its head and within the subtree itself.

        for subtree, depth in subtrees:
            original_dep = subtree.misc['original_dep']

            if is_prague_bridge_subtree(subtree):
                ch = [c for c in subtree.children if
                      c.misc['NodeType'] == 'Artificial' or
                      (c.xpos[0] in ['a', 'p', 'v', 'n', 't', 'l', 'm'] and
                       c.misc['original_dep'] not in ['AuxY', 'AuxZ']) ]
                if len(ch) == 1:
                    newh = ch[0]
                else:
                    logging.warning(f"Could not find a root candidate " +
                                f"for {subtree.address()}, deprel={subtree.deprel}, " +
                                f'len_ch={len(ch)}' )
                    continue
                self.redraw_subtree(newh, subtree)

            elif is_coord_subtree(subtree):
                # requires node.misc['CoordMember'] for coords
                members = [c for c in subtree.children if c.misc['CoordMember'] is True]
                if not members:
                    logging.error(f"No coordination members for {subtree.address()}")
                else:
                    first = members.pop(0)
                    first.parent = subtree.parent
                    for m in members:
                        m.parent = first
                        m.deprel = 'conj'

                    # temporarily, we attach the head of the coordination to the first conjunct, to avoid cycles
                    subtree.parent = first

                    # and all the remaining children of the previous head
                    for c in subtree.children:
                        c.parent = first
                        # we double-check that non-final coords (AuxY) are labeled `cc`
                        if c.misc['original_dep'] == 'AuxY' and c.upos == 'CCONJ':
                            c.deprel = 'cc'

                    if subtree.misc['NodeType'] == 'Artificial':
                        subtree.remove(children="warn")

                    # Now we reassign punctuations and coordinators (`cc`) where they belong (right conjunct)
                    for c in first.children:
                        if (c.udeprel == 'cc' or c.udeprel == 'punct') and c.precedes(first) is False:
                            self.attach_right(c, 'udeprel', 'conj')

            elif is_apos_subtree(subtree):
                members = [c for c in subtree.children if c.misc['AposMember'] == True]
                if not members:
                    logging.error(f"No apposition members for {subtree.address()}")
                else:
                    first = members.pop(0)
                    first.parent = subtree.parent
                    for m in members:
                        m.parent = first
                        m.deprel = 'apos'

                    # we reassign all its remaining children
                    for c in subtree.children:
                        c.parent = first

                    # now we assign the head of APOS to the first conj
                    if subtree.misc['NodeType'] == 'Artificial':
                        subtree.remove(children="warn")
                    else:
                        subtree.parent = first
                        subtree.deprel = 'punct' if subtree.upos == 'PUNCT' else subtree.deprel

            elif is_copula_subtree(subtree):
                try:
                    pnom = [c for c in subtree.children
                                if c.misc['original_dep'] == 'PNOM'][0]
                except IndexError:
                    logging.error(f"No PNOM for copula at {subtree.address()}?")
                    continue
                else:
                    pnom.deprel = subtree.deprel
                    self.redraw_subtree(pnom, subtree)
                    # pnom.deprel = subtree.deprel
                    # pnom.parent = subtree.parent
                    # subtree.parent = pnom

                    # for c in subtree.children:
                    #    c.parent = pnom

                    if subtree.misc['NodeType'] == 'Artificial':
                        subtree.remove(children="warn")
                    else:
                        subtree.parent = pnom
                        subtree.deprel = 'cop'

            elif is_ellipsis_subtree(subtree):
                chs = subtree.children
                original_head = subtree.parent

                if self._with_enhanced:
                    # TODO: if Artificial has lemma and morph, they should be replicated
                    # first we shift the artificial before the whole subtree
                    subtree.shift_before_subtree(subtree)
                    o = float(subtree.prev_node.ord)
                    # Now we create an empty node, and we calculate the new ord based on the right node
                    intid, dec = str(o).split(".")
                    empty = tree.create_empty_child()
                    # we set the morph properties of the empty node, if any
                    empty.upos = subtree.upos if subtree.upos else '_'
                    empty.lemma = subtree.lemma if subtree.lemma else '_'
                    empty.xpos = empty.xpos if empty.xpos else '_'
                    # ord and form
                    empty.ord = float(f'{intid}.{int(dec)+1}')
                    empty.form = f'E{empty.ord}'
                    logging.debug(f'Creating empty node at {tree.address()} {empty.form}')
                    # Now the dependencies of the empty nodes...
                    for c in chs:
                        c.deps.append({'parent': empty, 'deprel': c.deprel})
                        logging.warning(f'Deprel for nodes is: {c.raw_deps}')

                # now we seek for a node to promote
                # order: nsubj > obj > iobj > obl > advmod > csubj > xcomp > ccomp > advcl > dislocated > vocative
                order_list = ['nsubj', 'obj', 'iobj', 'obl', 'advmod', 'csubj', 'xcomp', 'ccomp', 'advcl', 'dislocated',
                              'vocative']
                newhead = get_first_in_priority(chs, order_list)
                if newhead:
                    newhead.deprel = subtree.deprel
                    self.redraw_subtree(newhead, subtree)
                else:
                    logging.error(f'Could not find candidates for promotion for {subtree.address()}')

                subtree.remove(children="warn")
