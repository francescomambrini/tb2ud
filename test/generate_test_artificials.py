"""
This script takes an AGDT xml file and generate a half-baked CONLL-U, right before the SetArtificial stage.
In this way, we create a test set to verify the problems in the SetArtificial stage.
"""

from udapi.core.document import Document
from udapi.block.agldt.setspaceafter import SetSpaceAfter
from udapi.block.read.agldt import Agldt as AgldtReader
from tb2ud import *
from tb2ud.text.updatetext import UpdateText
from tb2ud.postprocess.fixsomepos import FixSomePos
from collections import defaultdict
import re

tst_file = "./data/artificial_sentences.xml"

doc = Document()
reader = AgldtReader(tst_file, fix_cycles=True)
reader.apply_on_document(doc)
#trees = [b.get_tree() for b in doc.bundles]

blocks = [SetSpaceAfter(), CreateUpos(), CreateFeats(), SetMember(),
          ShallowConverter(), ShiftArtificials(),
          SubTreeConverter(with_enhanced=True), FixObj(),
          # SetArtificials(), MakeEnhanced(), # COMMENT OUT if you DO NOT want empty nodes and enhanced deps
          RehangPunct(), FixSomePos(), PurgeMisc(), UpdateText()]

for block in blocks:
    block.apply_on_document(doc)

doc.store_conllu("./data/non_transformed_artificials.conllu")