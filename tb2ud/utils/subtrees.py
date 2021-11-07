"""
At present just a random collection of snippets of code
"""


def get_depth(node, i=1):
    if node.parent.is_root():
        return i
    else:
        i += 1
        return get_depth(node.parent, i)


def get_subtree_depth(tree):
    nodes = tree.descendants
    no_leaves = [(n, get_depth(n)) for n in nodes if not n.is_leaf()]
    no_leaves.sort(key=lambda x : x[1], reverse=True)
    return no_leaves


def is_prague_bridge_subtree(subroot):
    """
    Analyze a subtree rooted in `subroot`. If the head of a tree has the deprel set
    to one of the PDT "bridge" functions (i.e. `AuxP` or `AuxC`) return True.
    Else, return False

    :param subroot: the root-node of a subtree
    :return: bool
    """
    if subroot.deprel in ['AuxC', 'AuxP']:
        return True
    else:
        return False


def is_coord_subtree(subroot):
    """
    Analyze a subtree rooted in `subroot`. If the head of a tree has the deprel set
    to `COORD` return True.
    Else, return False

    :param subroot: the root-node of a subtree
    :return: bool
    """
    if subroot.deprel == 'COORD':
        return True
    else:
        return False


def is_copula_subtree(subroot):
    """
    Contrary to all other subtrees, PNOM-subtrees cannot be redesigned by working only on the subtree
    rooted on the PNOM. Rather, the relevant subtree to work on is the one rooted on the governing copula.

    NOTE: this test, and the restructuring should take place before re-working ellipses; in fact, getting rid
    of "nominal" (i.e. non-coupular and non-verbal) clauses also means getting rid of many cases of ellipses.

    :param subroot: the root-node of a subtree
    :return: bool
    """
    childs = subroot.children
    for ch in childs:
        if ch.deprel == 'PNOM':
            return True
    return False


def is_ellipsis_subtree(subroot):
    if subroot.misc["NodeTypes"] == 'Artificial':
        return True
    else:
        return False