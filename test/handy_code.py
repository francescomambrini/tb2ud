from udapi.core.document import Document
from udapi.block.write.conllu import Conllu as ConlluWriter
from tb2ud.subtreeconverter import SubTreeConverter
from tb2ud.shiftartificials import ShiftArtificials

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
9	τῶν	ὁ	PRON	p-p---ng-	Case=Gen|Definite=Def|Gender=Neut|Number=Plur|PronType=Art	15	nmod	_	original_dep=ATR|Ref=543
10	ἐκείνης	ἐκεῖνος	DET	p-s---fg-	Case=Gen|Gender=Fem|Number=Sing|PronType=Dem	9	nmod	_	original_dep=ATR|Ref=543
11	ἔσχε	ἔχω	VERB	v3saia---	Mood=Ind|Number=Sing|Person=3|Tense=Past|Voice=Act	1	root	_	CoordMember|original_dep=PRED|Ref=543
12	δαίσασθαι	δαίνυμι	VERB	v--anm---	VerbForm=Inf|Voice=Mid	11	advcl	_	original_dep=ADV|Ref=543
13	πλέον	πλείων	ADJ	a-s---nac	Case=Acc|Degree=Cmp|Gender=Neut|Number=Sing	11	obl	_	original_dep=ADV|Ref=543|SpaceAfter=No
14	;	;	PUNCT	u--------	_	0	punct	_	original_dep=AuxK|Ref=543
15	[0]	_	_	_	_	16	obj	_	NodeType=Artificial|original_dep=OBJ
16	[1]	_	_	_	_	8	advcl	_	NodeType=Artificial|original_dep=ADV

"""

conllu_string1 = '''# sent_id = 162
# text = ὡς τοῖς λόγοις ἔνεστιν ἀμφοῖν κέρδος, εἰ σὺ μὲν μάθοις τοῖς τῆσδε χρῆσθαι, τοῖς δὲ σοῖς αὕτη πάλιν. [0] [1] [2]
1	ὡς	ὡς	SCONJ	c--------	_	22	mark	_	original_dep=AuxC|Ref=369
2	τοῖς	ὁ	DET	l-p---md-	Case=Dat|Definite=Def|Gender=Masc|Number=Plur|PronType=Art	3	det	_	original_dep=ATR|Ref=369
3	λόγοις	λόγος	NOUN	n-p---md-	Case=Dat|Gender=Masc|Number=Plur	4	obj	_	original_dep=OBJ|Ref=369
4	ἔνεστιν	ἔνειμι	VERB	v3spia---	Mood=Ind|Number=Sing|Person=3|Tense=Pres|Voice=Act	1	advcl	_	original_dep=ADV|Ref=370
5	ἀμφοῖν	ἄμφω	ADJ	a-d---fg-	Case=Gen|Gender=Fem|Number=Dual	3	nmod	_	original_dep=ATR|Ref=370
6	κέρδος	κέρδος	NOUN	n-s---nn-	Case=Nom|Gender=Neut|Number=Sing	4	nsubj	_	original_dep=SBJ|Ref=370|SpaceAfter=No
7	,	,	PUNCT	u--------	_	8	mark	_	original_dep=AuxC|Ref=370
8	εἰ	εἰ	SCONJ	c--------	_	4	mark	_	original_dep=AuxC|Ref=370
9	σὺ	σύ	PRON	p-s---fn-	Case=Nom|Gender=Fem|Number=Sing|Person=2|PronType=Prs	11	nsubj	_	original_dep=SBJ|Ref=370
10	μὲν	μέν	ADV	d--------	PartType=Ptcl	17	advmod	_	original_dep=AuxY|Ref=370
11	μάθοις	μανθάνω	VERB	v2saoa---	Mood=Opt|Number=Sing|Person=2|Voice=Act	17	advcl	_	CoordMember|original_dep=ADV|Ref=370
12	τοῖς	ὁ	DET	p-p---md-	Case=Dat|Definite=Def|Gender=Masc|Number=Plur|PronType=Art	14	obj	_	original_dep=OBJ|Ref=371
13	τῆσδε	ὅδε	DET	p-s---fg-	Case=Gen|Gender=Fem|Number=Sing|PronType=Dem	12	nmod	_	original_dep=ATR|Ref=371
14	χρῆσθαι	χράω	VERB	v--pne---	Tense=Pres|VerbForm=Inf|Voice=MidPass	11	ccomp	_	original_dep=OBJ|Ref=371|SpaceAfter=No
15	,	,	PUNCT	u--------	_	17	punct	_	original_dep=AuxX|Ref=371
16	τοῖς	ὁ	DET	l-p---md-	Case=Dat|Definite=Def|Gender=Masc|Number=Plur|PronType=Art	18	det	_	original_dep=ATR|Ref=371
17	δὲ	δέ	ADV	d--------	PartType=Ptcl	8	cc	_	original_dep=COORD|Ref=371
18	σοῖς	σός	DET	p-p---md-	Case=Dat|Gender=Masc|Number=Plur|Poss=Yes|PronType=Prs	23	obj	_	original_dep=OBJ|Ref=371
19	αὕτη	οὗτος	DET	p-s---fn-	Case=Nom|Gender=Fem|Number=Sing|PronType=Dem	24	nsubj	_	original_dep=SBJ|Ref=371
20	πάλιν	πάλιν	ADV	d--------	_	24	advmod	_	original_dep=AuxY|Ref=371|SpaceAfter=No
21	.	.	PUNCT	u--------	_	0	punct	_	original_dep=AuxK|Ref=371
22	[0]	_	_	_	_	0	root	_	NodeType=Artificial|original_dep=PRED
23	[1]	_	_	_	_	24	obj	_	NodeType=Artificial|original_dep=OBJ
24	[2]	_	_	_	_	17	advmod	_	CoordMember|NodeType=Artificial|original_dep=ADV
'''

def main():
    doc = Document()
    doc.from_conllu_string(conllu_string1)
    tree = doc.bundles[0].get_tree()
    nodes = tree.descendants
    writer = ConlluWriter()

    # Shifter
    shifter = ShiftArtificials()
    shifter.apply_on_document(doc)

    writer.apply_on_document(doc)

    # Converter
    converter = SubTreeConverter(with_enhanced=True)
    converter.apply_on_document(doc)

    print(len(tree.empty_nodes))

    # Writer
    writer.apply_on_document(doc)


if __name__ == '__main__':
    main()
