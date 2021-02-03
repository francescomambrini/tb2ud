from udapi.core.block import Block
import logging

# ADV
# AuxY
# AuxZ

negs = ['μήτε', 'μηδέ', 'οὐδέ', 'οὐ', 'μή',
         'οὐδέ', 'οὐδέ', 'οὔτε', 'οὐδείς']

class ShallowConverter(Block):
    """
    Performs a shallow mapping between the AGLDT deprel labels with the UD ones.

    By shallow mapping, we mean a mapping between the deprel labels where no
    subtree is restructured. Thus, this script works node by node and it won't
    rearrange the tree, not even in the case of structures that must be changed
    from one schema to the other (like e.g. the nominal predicate labeled as PNOM).

    Use `SubTreeConverter` to restructure the trees according to the UD guidelines.
    """

    @staticmethod
    def artificial_is_verb(artinode):
        conds = (artinode.parent.misc['original_dep'] == 'AuxC',
                 len([c for c in artinode.children if c.deprel in ('OBJ', 'SBJ', 'PNOM')]) > 1)
        if artinode.misc['NodeType'] != 'Artificial':
            return False
        else:
            if any(conds):
                return True


    def process_node(self, node):
        dep = node.deprel.split("_")[0]
        node.misc['original_dep'] = dep

        # PRED
        if dep == 'PRED':
            if node.misc['original_dep'] == 'PRED_PA':
                node.deprel = 'parataxis'
            else:
                node.deprel = 'root'

        # SBJ
        elif dep == 'SBJ':
            if node.xpos[0] == 'v' and node.xpos[4] != 'p':
                node.deprel = 'csubj'
            else:
                node.deprel = 'nsubj'

        # OBJ
        elif dep == 'OBJ':
        # OBJ has many interpretations! Further distinctions between obj, obl, iobj
        # will be handled in a specific postprocessing step. Here we just catch
        # the the easiest cases
            h = node.parent
            if h.deprel == 'AuxP':
                node.deprel = 'obl'
            elif node.xpos[0] == 'v' and node.xpos[4] != 'p':
                node.deprel = 'ccomp'
            else:
                node.deprel = 'obj'

        # ADV
        elif dep == 'ADV':
            if node.xpos[0] in ['n', 'p', 'a']:
                node.deprel = 'obl'
            elif node.xpos[0] == 'v' and node.xpos[4] != 'p':
                node.deprel = 'advcl'
            # participles tagged ADV are advcl unless they are substantivized
            # we try to catch them by looking for an article, even this is not
            # 100% the case...
            elif node.xpos[0] in ['v', 't'] and node.xpos[4] == 'p':
                node.deprel = 'advcl'
                for c in node.children:
                    if c.xpos[0] == 'l':
                        node.deprel = 'obl'
            elif node.misc['NodeType'] == 'Artificial' and self.artificial_is_verb(node):
                node.deprel = 'advcl'
            else:
                node.deprel = 'advmod'

        # ATR
        elif dep == 'ATR':
            # if the ATR node is an indicative, optative or subj. verb
            # then it's the head of a relative clause
            if node.xpos[0] == 'l' or node.upos == 'DET':
                node.deprel = 'det'
            elif node.xpos[0] == 'm':
                node.deprel = 'nummod'
            elif node.xpos[0] == 'v' and node.xpos[4] in ['i', 's', 'o']:
                node.deprel = 'acl:relcl'
            elif node.xpos[0] == 'v' and node.xpos[4] == 'n':
                node.deprel = 'acl'
            elif node.xpos[0] == 'a':
                node.deprel = 'amod'
            # attributive participles are also treated like adjectives
            # but we fix them in postprocessing, as we need syntax to
            # distinguish them from substantivized genitives
            else:
                node.deprel = 'nmod'

        # OCOMP
        elif dep == 'OCOMP':
            node.deprel = 'xcomp'

        # ATV
        # Praedicativa (à la Pinkster) are hard to render: if they have a noun
        # they can be attached to (ATV in PDT style), they become secondary predication
        # of the acl type; if not, then they are treated as advcl. But just in case,
        # we keep a new subtype `compl` to mark them...
        elif dep == 'ATV':
            node.deprel = 'acl:compl'

        # AtvV
        elif dep == 'AtvV':
            node.deprel = 'advcl:compl'

        # COORD
        elif dep == 'COORD':
            node.deprel = 'cc'

        # PNOM
        elif dep == 'PNOM':
        # All PNOM become xcomp, we'll take care to fix copular and nominal
        # constructions in the SubTreeConverter module
            node.deprel = "xcomp"

        # APOS
        elif dep == 'APOS':
            node.deprel = 'dep:apos'

        # AuxV
        elif dep == 'AuxV':
            node.deprel = 'aux'

        # AuxP
        elif dep == 'AuxP':
            node.deprel = 'case'

        # AuxC
        elif dep == 'AuxC':
            node.deprel = 'mark'

        # AuxX/AuxK/AuxG
        elif dep in ['AuxK', 'AuxX', 'AuxG']:
            node.deprel = 'punct'

        # ExD
        elif dep == 'ExD':
            if node.misc["NodeType"] == 'Artificial':
                # TODO: verify!
                # actually, I am not sure...
                'vocative'
            elif node.xpos[7] in ['n', 'v']:
                node.deprel = 'vocative'
            elif node.xpos[0] in ['e', 'i']:
                node.deprel = 'discourse'
            else:
                node.deprel = 'orphan'

        # AuxZ
        elif dep == 'AuxZ':
            if node.lemma in negs:
                node.deprel = 'advmod:neg'
            elif node.xpos[0] == 'r':
                node.deprel = 'compound:prt'
            else:
                node.deprel = 'advmod'

        # AuxY
        # Most likely, we'll need a special module for particles tagged as AuxY,
        # built on a lemma based...
        elif dep == 'AuxY':
            head = node.parent
            if head.misc['original_dep'] == 'COORD':
                node.deprel = 'cc'
            # occasionally, AuxY is used for emphatically repeated words
            elif node.lemma == head.lemma:
                node.deprel = 'discourse'
            # sometimes it is used with parenthetical verbs, like οἶδα
            elif node.xpos[0] == 'v':
                # if it is intoduced by a conj it is an advcl (it happens with Gorman trees)
                if node.parent.upos == 'SCONJ':
                    node.deprel = 'advcl'
                    node.misc['original_dep'] = 'ADV'
                else:
                    node.deprel = 'parataxis'
            # another potential use is with MWEs, where "fixed" is to be used
            # but I can't come up with an AG example of that...
            else:
                node.deprel = 'advmod'

        # XSEG
        elif dep == 'XSEG':
            node.deprel = 'goeswith'

        else:
            node.deprel = 'dep'
            logging.warning(f"Could not guess a deprel for node {node.address()} ({node.misc['original_dep']})")

        # Final check for specific POS-based assignments
        if node.xpos[0] in ['e', 'i']:
            node.deprel = 'discourse'
