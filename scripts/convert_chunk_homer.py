import argparse
from udapi.core.document import Document
from udapi.block.write.conllu import Conllu as ConlluWriter
from udapi.block.agldt.setspaceafter import SetSpaceAfter
from udapi.block.read.agldt import Agldt as AgldtReader
from udapi.block.agldt.createupos import CreateUpos
from udapi.block.agldt.createfeats import CreateFeats
from tb2ud import *
from tb2ud.text.updatetext import UpdateText
from tb2ud.postprocess.fixsomepos import FixSomePos

parser = argparse.ArgumentParser()
parser.add_argument("infile", help="input file")
parser.add_argument('-s', '--start', type=int, default=1, help='Starting book')
parser.add_argument('-e', '--end', type=int, default=24, help='Ending book')
args = parser.parse_args()

doc = Document()
reader = AgldtReader(args['infile'])
reader.apply_on_document(doc)

blocks = [SetSpaceAfter(), CreateUpos(), CreateFeats(), SetMember(),
          ShallowConverter(), ShiftArtificials(),
          SubTreeConverter(with_enhanced=True),
          FixObj(), # Skipping MakeEnhanced for now
          RehangPunct(), FixSomePos(), PurgeMisc(), UpdateText()]


# udapy read.Agldt files="$1" \
#   agldt.SetSpaceAfter \
#   agldt.CreateUpos \
#   agldt.CreateFeats \
#   .SetMember \
#   .ShallowConverter \
#   .ShiftArtificials \
#   .SubTreeConverter with_enhanced="True" \
#   .FixObj \
#   .RehangPunct \
#   .MakeEnhanced \
#   .postprocess.FixSomePos \
#   .PurgeMisc \
#   .text.UpdateText \
#   util.Eval doc='doc.meta["docname"]=doc.meta["loaded_from"][:-4]+".conllu"' \
#   write.Conllu docname_as_file=1
