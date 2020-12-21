import logging

from udapi.core.block import Block
from udapi.block.agldt.agldt_util.subtrees import get_subtree_depth
from tb2ud.utils.constructions import *
from tb2ud.utils import get_first_in_priority

# create a named tuple to map empty nodes: parent_rel is a tuple (head, deprel),
# dep_list a list of tuples (dependent, rel)


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
        # TODO: attachment of cc must be fixed: 1. cc with the first conj 2. correct positioning of postpositive conjs
        h = element.parent
        right_bros = [ch for ch in h.children if ch.precedes(element) is False]
        if element.lemma in ['τε', '-τε', 'δέ']:
            right_bros.append(element.prev_node)
        for b in right_bros:
            checked_val = getattr(b, attr)
            if checked_val == val:
                element.parent = b
                return None

    @staticmethod
    def write_deps_in_misc(tree):
        """
        Records the dependency relation in the `misc` column in case:
        - a node is artificial
        - a non-artificial node depends on an artificial head.

        Parameters
        ----------
        tree: udapi Root
            the whole sentence tree

        """
        for n in tree.descendants:
            if n.misc['NodeType'] == 'Artificial' or n.parent.misc['NodeType'] == 'Artificial':
                # n.deps.append({'parent': n.parent, 'deprel': n.deprel})
                n.misc['art_deps'] = f'{n.parent.ord}%:%{n.deprel}'

    #         self.delete_deps_to_art(art, tree, warning=True)

    def process_tree(self, tree):
        subtrees = get_subtree_depth(tree)
        arts = [n for n in tree.descendants if n.misc['NodeType'] == 'Artificial']
        arts_on_arts = [a for a in arts if a.parent in arts]
        art_original_children = {a: a.children for a in arts}
        art_original_heads = {a: a.parent for a in arts}
        if self._with_enhanced:
            self.write_deps_in_misc(tree)
            for a in arts:
                a.misc['original_ord'] = str(a.ord)

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

                # TODO: work with shared modifiers
                # shared = [c for c in subtree.children if c.misc['CoordMember'] is False]
                for c in subtree.children:
                    if c not in members and c.misc['original_dep'] not in ['AuxY', 'AuxX', 'AuxZ']:
                        c.misc['SharedMod'] = 'True'
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
                        # self.delete_deps_to_art(subtree, tree, warning=True)

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
                        m.deprel = 'appos'

                    # we reassign all its remaining children
                    for c in subtree.children:
                        c.parent = first

                    # now we assign the head of APOS to the first conj
                    if subtree.misc['NodeType'] == 'Artificial':
                        subtree.remove(children="warn")
                        #arts.remove(subtree)
                        # self.delete_deps_to_art(subtree, tree, warning=True)

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
                    # prep phrases as pnom are not transformed
                    if 'case' in [c.deprel for c in pnom.children]:
                        pnom.deprel = 'obl'
                        continue
                    pnom.deprel = subtree.deprel
                    self.redraw_subtree(pnom, subtree)
                    # pnom.deprel = subtree.deprel
                    # pnom.parent = subtree.parent
                    # subtree.parent = pnom

                    if subtree.upos == 'VERB':
                        subtree.upos = 'AUX'

                    # for c in subtree.children:
                    #    c.parent = pnom

                    if subtree.misc['NodeType'] == 'Artificial':
                        subtree.remove(children="warn")
                        logging.debug(f'Removing node {subtree.address()}, {subtree.misc["original_dep"]}')
                        # self.delete_deps_to_art(subtree, tree, warning=True)
                    else:
                        subtree.parent = pnom
                        subtree.deprel = 'cop'

            # elif is_ell_comparative(subtree):
            #     chs = subtree.children
            #     sub = None
            #     for i, c in enumerate(chs):
            #         if c.misc['original_dep'] == 'SBJ':
            #             sub = chs.pop(i)
            #             break
            #     if sub:
            #         sub.deprel = subtree.deprel
            #         self.redraw_subtree(sub, subtree)
            #         for c in chs:
            #             c.misc['orphaned'] = 'True'
            #     else:
            #         logging.error(f'Node {subtree.address()}, {subtree.form} should be head of simile, but no SBJ found')

        #     elif is_ellipsis_subtree(subtree):
        #         chs = subtree.children
        #         # original_head = subtree.parent
        #
        #         # if self._with_enhanced:
        #         #     # original_head.deps.append({'parent': subtree, 'deprel': subtree.deprel})
        #         #     subtree.deps.append({'parent': original_head, 'deprel': subtree.deprel})
        #         #     for c in chs:
        #         #         c.deps.append({'parent': subtree, 'deprel': c.deprel})
        #
        #         # now we seek for a node to promote
        #         # order: nsubj > obj > iobj > obl > advmod > csubj > xcomp > ccomp > advcl > dislocated > vocative
        #         order_list = ['nsubj', 'obj', 'iobj', 'obl', 'advmod', 'csubj', 'xcomp', 'ccomp', 'advcl', 'dislocated',
        #                       'vocative', 'nmod']
        #         newhead = get_first_in_priority(chs, order_list)
        #         if newhead:
        #             newhead.deprel = subtree.deprel
        #             self.redraw_subtree(newhead, subtree)
        #             left_chs = [c for c in chs if c is not newhead]
        #             for left_c in left_chs:
        #                 if left_c.udeprel in order_list and left_c.xpos[0] in ['a', 'v', 'n', 'p']:
        #                     left_c.misc['orphaned'] = 'True'
        #         else:
        #             logging.error(f'Could not find candidates for promotion for {subtree.address()}, {subtree.form}')
        #
        # if self._with_enhanced:
        #     remaining_arts = [n for n in tree.descendants if n.misc['NodeType'] == 'Artificial']
        #     empty_maps = self.copy_to_empty(remaining_arts, tree, art_original_heads, art_original_children, arts_on_arts)
        #     art_mapping = {str(e.misc['original_ord']): e for e in tree.empty_nodes}
        #     if remaining_arts:
        #         for e in empty_maps:
        #             enods = [e.emptynode for e in empty_maps]
        #             # that sets the deps from empty to head of former artificial
        #             e.emptynode.deps.append({'parent': e.parent_rel[0], 'deprel': e.parent_rel[1]})
        #
        #             # that should take care of deps of the empty nodes
        #             empty_childs = e.dep_list
        #             for ech in empty_childs:
        #                 if ech[0] in tree.descendants:
        #                     ech[0].deps.append({'parent': e.emptynode, 'deprel': ech[1]})

                # for node in tree.descendants:
                    # if node.misc['art_deps']:
                    #     dep_head, dep_rel = node.misc['art_deps'].split("%:%")
                    #     try:
                    #         node.deps.append({'parent': art_mapping[dep_head], 'deprel': dep_rel})
                    #     except KeyError:
                    #         continue
