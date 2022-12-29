from udapi.core.document import Document
from udapi.block.write.conllu import Conllu
from io import StringIO
import sys

doc = Document()
doc.load_conllu('data/coord_sentences.conllu')

if __name__ == '__main__':
    fh = StringIO()
    old_stdout = sys.stdout
    sys.stdout = fh

    writer = Conllu()
    writer.apply_on_document(doc)

    output = fh.getvalue()
    sys.stdout = old_stdout
    s = doc.to_conllu_string()
    print("Printing string!\n\n" + s)
    #print(output[:50])
    
