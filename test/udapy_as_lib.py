"""
Code to showcase how to use `udapi` as a library in Python code
"""

from udapi.block.read.pedalion import Pedalion
from udapi.block.read.agldt import Agldt as AgldtReader
from udapi.core.document import Document
from udapi.block.write.conllu import Conllu as ConlluWriter

ex_file = 'data/hdt-1-20-39-bu2.xml'

doc = Document()
reader = AgldtReader(ex_file)
reader.apply_on_document(doc)
conlluwr = ConlluWriter()

# diagnostica varia
bun = doc.bundles[0]
tree = bun.trees[0]
nodes = tree.descendants
for n in nodes:
    print(n.form, n.xpos)

