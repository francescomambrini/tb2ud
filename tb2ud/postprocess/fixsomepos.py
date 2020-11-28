from udapi.core.block import Block
from tb2ud.utils.constructions import is_used_adjectively
# from udapi.block.agldt.createupos import dets


class FixSomePos(Block):
    def process_node(self, node):
        
        # fix adverbs tagged as conj
        if node.udeprel == 'advmod' and node.upos in ['SCONJ', 'CCONJ']:
            node.upos = 'ADV'

        # which DET is actually a DET and which is a PRON?
        if node.upos == 'DET':
            if is_used_adjectively(node):
                node.deprel = 'det'
            else:
                node.upos = 'PRON'
                if node.udeprel == 'det':
                    node.deprel = 'nmod'

        # attributive participles are all nmod
        if node.feats['VerbForm'] == 'Part' and node.deprel == 'nmod':
            if is_used_adjectively(node):
                node.deprel = 'amod'
