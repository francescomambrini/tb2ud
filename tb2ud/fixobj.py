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

class FixObj(Block):

    def process_node(self, node):
        # TODO: postprocess the different constructions tagged as OBJ
        pass
