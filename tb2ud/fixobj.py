"""
This module takes care of fixing the conversion of AGLDT's OBJs to UD.
OBJ in the PDT-style annotation is used for almost all 2nd valency argument.
However, UD is based on the Core/Periphery distinction, not on Argument-vs-Adjunct.

Therefore, OBJ can stand for UD's:
* obj (direct core verbal argument)
* iobj (indirect obj, 3rd core argument)
* obl (non-core)

The distinction is not easy at all!

"""

from udapi.core.block import Block
import logging


class FixObj(Block):

    def process_node(self, node):
        # TODO: postprocess the different constructions tagged as OBJ
        objs = [n for n in node.children if n.udeprel == 'obj']
        if len(objs) > 1:
            accs = [o for o in objs if o.feats['Case'] == 'Acc']
            dats = [o for o in objs if o.feats['Case'] == 'Dat']
            for o in objs:
                if 'case' in [c.udeprel for c in o.children]:
                    o.deprel = 'obl:arg'
                elif o in dats and accs:
                    o.deprel = 'iobj'

            if len([c for c in node.children if c.udeprel == 'obj']) > 1:
                logging.warning(f'Node {node.address()} has more than 2 obj\'s, but I can\'t sort them out')
