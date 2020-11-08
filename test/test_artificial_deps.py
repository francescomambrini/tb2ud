import unittest
import os

from udapi.core.root import Root
from udapi.core.document import Document
from udapi.block.write.conllu import Conllu as ConlluWriter
from tb2ud.subtreeconverter import SubTreeConverter

# loaded from the file: electra_shallow.conllu
conllu_string = """# sent_id = 264
# text = ἢ τῶν ἐμῶν Ἅιδης τιν' ἵμερον τέκνων ἢ τῶν ἐκείνης ἔσχε δαίσασθαι πλέον; [0] [1]
1	ἢ	ἤ	CCONJ	c--------	_	0	cc	_	original_dep=COORD|Ref=542
2	τῶν	ὁ	DET	l-p---ng-	Case=Gen|Definite=Def|Gender=Neut|Number=Plur|PronType=Art	7	det	_	original_dep=ATR|Ref=542
3	ἐμῶν	ἐμός	DET	p-p---ng-	Case=Gen|Gender=Neut|Number=Plur|Poss=Yes|PronType=Prs	7	nmod	_	original_dep=ATR|Ref=542
4	Ἅιδης	ᾍδης	PROPN	n-s---mn-	Case=Nom|Gender=Masc|Number=Sing	11	nsubj	_	original_dep=SBJ|Ref=542
5	τιν'	τις	DET	p-s---ma-	Case=Acc|Gender=Masc|Number=Sing|PronType=Ind	6	nmod	_	original_dep=ATR|Ref=542
6	ἵμερον	ἵμερος	NOUN	n-s---ma-	Case=Acc|Gender=Masc|Number=Sing	11	obj	_	original_dep=OBJ|Ref=542
7	τέκνων	τέκνον	NOUN	n-p---ng-	Case=Gen|Gender=Neut|Number=Plur	6	nmod	_	original_dep=ATR|Ref=542
8	ἢ	ἤ	CCONJ	c--------	_	13	mark	_	original_dep=AuxC|Ref=543
9	τῶν	ὁ	DET	p-p---ng-	Case=Gen|Definite=Def|Gender=Neut|Number=Plur|PronType=Art	15	nmod	_	original_dep=ATR|Ref=543
10	ἐκείνης	ἐκεῖνος	DET	p-s---fg-	Case=Gen|Gender=Fem|Number=Sing|PronType=Dem	9	nmod	_	original_dep=ATR|Ref=543
11	ἔσχε	ἔχω	VERB	v3saia---	Mood=Ind|Number=Sing|Person=3|Tense=Past|Voice=Act	1	root	_	CoordMember|original_dep=PRED|Ref=543
12	δαίσασθαι	δαίνυμι	VERB	v--anm---	VerbForm=Inf|Voice=Mid	11	advcl	_	original_dep=ADV|Ref=543
13	πλέον	πλείων	ADJ	a-s---nac	Case=Acc|Degree=Cmp|Gender=Neut|Number=Sing	11	obl	_	original_dep=ADV|Ref=543|SpaceAfter=No
14	;	;	PUNCT	u--------	_	0	punct	_	original_dep=AuxK|Ref=543
15	[0]	_	_	_	_	16	obj	_	NodeType=Artificial|original_dep=OBJ
16	[1]	_	_	_	_	8	advcl	_	NodeType=Artificial|original_dep=ADV

"""


class TestEnhDeps(unittest.TestCase):
    """Unit tests for udapi.core.node and enhanced dependecies.
    Tests the behaviour with empty nodes (with decimal ord, such as 0.1, 2.3 etc.) as well"""

    @classmethod
    def setUpClass(cls):
        cls.doc = Document()
        # cls.data = os.path.join(os.path.dirname(tb2ud.__file__), "../test/data/tlg0011.tlg005.daphne_tb-grc1.xml")
        cls.doc.from_conllu_string(conllu_string)
        cls.tree = cls.doc.bundles[0].get_tree()
        cls.nodes = cls.tree.descendants
        cls.writer = ConlluWriter()
        cls._subtreeconverted = False

    def apply_converter(self):
        if not self._subtreeconverted:
            converter = SubTreeConverter(with_enhanced=True)
            converter.apply_on_document(self.doc)
            self._subtreeconverted = True

    def test_reading(self):
        self.assertEqual('Artificial', self.nodes[-1].misc['NodeType'])

    def test_subtree_conversion(self):
        self.apply_converter()
        empties = self.tree.empty_nodes
        self.assertEqual(len(empties), 2)

        self.writer.apply_on_document(self.doc)
