"""
# TODO better support for transition Artificial > Empty
should be DEPRECATED soon! It has a lot of problems.
E.g.:
1. duplicates some dependencies (some nodes have double deps to the empty)
2. too much rubbish (punctuation, AuxY etc should not have deps to empty)
3. less empty nodes should be created

"""


from udapi.core.block import Block
from tb2ud.utils import get_first_in_priority
import logging
from collections import namedtuple


Emptymap = namedtuple('Emptymap', 'emptynode oldord parent_rel dep_list')


def redraw_subtree(new_head, current_head):
    subhead = current_head.parent

    new_head.parent = subhead
    current_head.parent = new_head

    for c in current_head.children:
        if c.udeprel != 'goeswith':
            c.parent = new_head


def copy_to_empty(artificials, tree, heads_of_arts, children_of_arts, second_level_arts):
    """
    Makes a copy of the artificial nodes, and attaches them to the root of the sentence.
    It also deletes (with rehanging of the child nodes) the original artificial nodes.
    (rehanging is needed, because a child of an artificial could be a still unresolved artificial)

    Parameters
    ----------
    artificials : iterable
        iterable with all the artificial nodes

    tree : Root
        the sentence tree

    heads_of_arts : dict
        dictionary of ArtificialNode: parent node of art

    children_of_arts : dict
        dictionary ArtificialNode: its children

    second_level_arts : iter
        list or iterable with all artificial that depends on another artificial

    Returns
    -------
    list of Namedtuple (Emptymap)
    """

    def set_empty_ord(n, root, iteration=1):
        empty_ords = [e.ord for e in root.empty_nodes]
        neword = float(f'{n.prev_node.ord}.{iteration}')
        if neword in empty_ords:
            neword = set_empty_ord(n, root, iteration=iteration+1)
        return neword

    empty_maps = []

    for art in artificials:
        lemma = art.lemma if art.lemma else None
        upos = art.upos if art.upos else None
        xpos = art.xpos if art.xpos else None
        feats = art.feats if art.feats else None
        ord_id = set_empty_ord(art, tree)
        form = f'E{ord_id}'
        empty = tree.create_empty_child(form=form, lemma=lemma, upos=upos, xpos=xpos,
                                        feats=feats)
        logging.debug(f'Creating empty node at {tree.address()} {empty.form}')

        # we set the ord now
        empty.ord = float(ord_id)

        # we also set some important misc values
        empty.misc = {'original_dep': art.misc.get('original_dep'),
                      'AposMember': art.misc.get('AposMember'),
                      'CoordMember': art.misc.get('CoordMember'),
                      'art_deps': art.misc.get('art_deps'),
                      'original_ord': str(art.misc['original_ord'])}

        eparent = ''
        if art not in second_level_arts:
            eparent = heads_of_arts[art]
        else:
            for en in empty_maps:
                for c in en.dep_list:
                    if c[0] == art:
                        eparent = en.emptynode
        if eparent == '':
            eparent = art.root
            logging.error(f"Couldn't find a parent for articial node {art.root.address},{empty.form} ({art.form})")

        emap = Emptymap(empty, art.ord, (eparent, art.deprel), [(c, c.deprel) for c in children_of_arts[art] if
                                                                c.misc['original_dep'] not in ['AuxX', 'AuxY']])

        art.remove(children='rehang')
        empty_maps.append(emap)

    return empty_maps


class SetArtificials(Block):

    def process_tree(self, tree):
        arts = [n for n in tree.descendants if n.misc['NodeType'] == 'Artificial']
        arts_on_arts = [a for a in arts if a.parent in arts]
        art_original_children = {a: a.children for a in arts}
        art_original_heads = {a: a.parent for a in arts}
        for node in tree.descendants:
            if node.misc['NodeType'] == 'Artificial':

                chs = node.children
                order_list = ['nsubj', 'obj', 'iobj', 'obl', 'advmod', 'csubj', 'xcomp', 'ccomp', 'advcl', 'dislocated',
                              'vocative', 'nmod']
                newhead = get_first_in_priority(chs, order_list)
                if newhead:
                    newhead.deprel = node.deprel
                    redraw_subtree(newhead, node)
                    left_chs = [c for c in chs if c is not newhead]
                    for left_c in left_chs:
                        if left_c.udeprel in order_list and left_c.xpos[0] in ['a', 'v', 'n', 'p']:
                            left_c.misc['orphaned'] = 'True'
                else:
                    logging.error(f'Could not find candidates for promotion for {node.address()}, {node.form}')

        # set the enhanced
        remaining_arts = [n for n in tree.descendants if n.misc['NodeType'] == 'Artificial']
        empty_maps = copy_to_empty(remaining_arts, tree, art_original_heads, art_original_children, arts_on_arts)
        art_mapping = {str(e.misc['original_ord']): e for e in tree.empty_nodes}
        if remaining_arts:
            for e in empty_maps:
                enods = [e.emptynode for e in empty_maps]
                # that sets the deps from empty to head of former artificial
                e.emptynode.deps.append({'parent': e.parent_rel[0], 'deprel': e.parent_rel[1]})

                # that should take care of deps of the empty nodes
                empty_childs = e.dep_list
                for ech in empty_childs:
                    if ech[0] in tree.descendants:
                        ech[0].deps.append({'parent': e.emptynode, 'deprel': ech[1]})

        for node in tree.descendants:
            if node.misc['art_deps']:
                dep_head, dep_rel = node.misc['art_deps'].split("%:%")
                try:
                    node.deps.append({'parent': art_mapping[dep_head], 'deprel': dep_rel})
                except KeyError:
                    continue