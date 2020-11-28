def is_prague_bridge_subtree(subroot):
    """
    Analyze a subtree rooted in `subroot`. If the head of a tree has the misc['original_dep'] set
    to one of the PDT "bridge" functions (i.e. `AuxP` or `AuxC`) return True.
    Else, return False

    :param subroot: the root-node of a subtree
    :return: bool
    """
    if subroot.misc['original_dep'] in ['AuxC', 'AuxP']:
        return True
    else:
        return False


def is_conj_with_elided_subtree(subroot):
    """
    If the head of the subtree is a PDT-style AuxC governing an elided subtree,
    we need a bit of supplementary thinking (can be a simile, a comparative...)
    """
    if subroot.misc['original_dep'] == 'AuxC' and \
                subroot.misc['NodeType'] == 'Artificial':
        return True
    else:
        return False


def is_coord_subtree(subroot):
    """
    Analyze a subtree rooted in `subroot`. If the head of a tree has the misc['original_dep'] set
    to `COORD` return True.
    Else, return False

    :param subroot: the root-node of a subtree
    :return: bool
    """
    if subroot.misc['original_dep'] == 'COORD':
        return True
    else:
        return False


def is_apos_subtree(subroot):
    """
    Analyze a subtree rooted in `subroot`. If the head of a tree has the misc['original_dep'] set
    to `APOS` return True.
    Else, return False

    :param subroot: the root-node of a subtree
    :return: bool
    """
    if subroot.misc['original_dep'] == 'APOS':
        return True
    else:
        return False


def is_copula_subtree(subroot):
    """
    Contrary to all other subtrees, PNOM-subtrees cannot be redesigned by working only on the sequence of nodes
    rooted on the PNOM. Rather, the relevant subtree to work on is the one rooted on the governing copula.

    NOTE: this test, and the restructuring should take place before re-working ellipses; in fact, getting rid
    of "nominal" (i.e. non-coupular and non-verbal) clauses also means getting rid of many cases of ellipses.

    :param subroot: the root-node of a subtree
    :return: bool
    """
    if subroot.lemma == 'εἰμί' or subroot.misc['NodeType'] == 'Artificial':
        childs = subroot.children
        for ch in childs:
            if ch.misc['original_dep'] == 'PNOM':
                return True
    return False


def is_ellipsis_subtree(subroot):
    if subroot.misc["NodeType"] == 'Artificial':
        return True
    else:
        return False


def is_ell_comparative(subroot):
    """
    Checks whether a subtree is a simile/comparative clause with verb elided. In the AGLDT-like formalism,
    all comparatives are annotated as clauses, e.g.:

    "He jumped like a lion" --> "He jumped like a lion [jumps]"

    We keep the empty node for the clause verb

    Parameters
    ----------
    subroot : Node
        the head of the subtree

    Returns
    -------
    bool
    """
    if is_ellipsis_subtree(subroot):
        if subroot.parent.lemma in ['ὡς', 'ἠύτε']:
            return True


def is_used_adjectively(node):
    """
    Check if a word (especially a DET) is used adjectivelly or pronominally

    Parameters
    ----------
    node : udapi.core.node.Node

    Returns
    -------
    bool

    """
    parent = node.parent
    conditions = (node.udeprel in ['amod', 'det', 'nmod'],
                  node.feats['Gender'] == parent.feats['Gender'],
                  node.feats['Case'] == parent.feats['Case'],
                  node.feats['Number'] == parent.feats['Number'])
    return all(conditions)
