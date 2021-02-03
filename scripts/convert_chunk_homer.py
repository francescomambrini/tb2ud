#!/usr/bin/env python

import argparse
from udapi.core.document import Document
from udapi.block.agldt.setspaceafter import SetSpaceAfter
from udapi.block.read.agldt import Agldt as AgldtReader
from tb2ud import *
from tb2ud.text.updatetext import UpdateText
from tb2ud.postprocess.fixsomepos import FixSomePos
from collections import defaultdict
import re


def get_first_with_ref(node_zero):
    next_node = node_zero.next_node
    reg = re.compile(r'[0-9]+\.[0-9]+')
    if reg.search(next_node.misc['Ref']):
        return next_node
    else:
        get_first_with_ref(next_node)


def get_ordered_trees(trees, book_start: int, book_end: int):
    d = defaultdict(list)
    print("creating the dictionary")
    for i, tree in enumerate(trees):
        nn = get_first_with_ref(tree)
        bk, ln = nn.misc['Ref'].split('.')
        if book_start <= int(bk) <= book_end:
            d[int(bk)].append((int(ln), tree))
    print("reordering the dictionary")
    for k in d.keys():
        d[k].sort(key=lambda x: x[0])
    return d


parser = argparse.ArgumentParser()
parser.add_argument("infile", help="Input file")
parser.add_argument('-s', '--start', type=int, default=1, help='Starting book')
parser.add_argument('-e', '--end', type=int, default=24, help='Ending book')
parser.add_argument('-o', '--out', help='Output file')
args = parser.parse_args()

doc = Document()
reader = AgldtReader(args.infile, fix_cycles=True)
reader.apply_on_document(doc)
trees = [b.get_tree() for b in doc.bundles]
tree_dic = get_ordered_trees(trees, args.start, args.end)
book_list = sorted(tree_dic.keys())

ordered_doc = Document()

for book in book_list:
    for _, sent in tree_dic[book]:
        bund = ordered_doc.create_bundle()
        bund.add_tree(sent)

outname = args.out

blocks = [SetSpaceAfter(), CreateUpos(), CreateFeats(), SetMember(),
          ShallowConverter(), ShiftArtificials(),
          SubTreeConverter(with_enhanced=True), FixObj(),
          SetArtificials(), MakeEnhanced(), # COMMENT OUT if you DO NOT want empty nodes and enhanced deps
          RehangPunct(), FixSomePos(), PurgeMisc(), UpdateText()]


for block in blocks:
    block.apply_on_document(ordered_doc)

if outname:
    ordered_doc.store_conllu(outname)
