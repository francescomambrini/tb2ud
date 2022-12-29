#!/usr/bin/env python3

import os
import pyconll
from glob import glob

# INPUT directory
pdir = '/home/francesco/Documents/work/Progetti/katholou/ud_treebanks/daphne/data'

pths = glob(os.path.join(pdir, '*.conllu'))
c = pyconll.load_from_file(pths[0])

os.path.basename(pths[0])
auth,tit = os.path.basename(pths[0]).split('.')[0:2]

for sent in c:
    sent.id = f'{auth}.{tit}.{sent.id}'
    
i = len(c)
for f in pths[1:]:
    auth, tit = os.path.basename(f).split('.')[:2]
    text_conll = pyconll.iter_from_file(f)
    for sent in text_conll:
        sent.id = f'{auth}.{tit}.{sent.id}'
        c.insert(i, sent)
        i += 1

# OUTPUT filename
outpth = '/home/francesco/Desktop/daphne.conllu'  

with open(outpth, 'w') as out:
    c.write(out)      
