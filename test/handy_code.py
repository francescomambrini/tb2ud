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

conllu_string1 = '''# sent_id = 265
# text = ἢ τῷ πανώλει πατρὶ τῶν μὲν ἐξ ἐμοῦ παίδων πόθος παρεῖτο, Μενέλεω δ' ἐνῆν; [0] [1]
1	ἢ	ἤ	CCONJ	c--------	_	0	cc	_	original_dep=COORD|Ref=544
2	τῷ	ὁ	DET	l-s---md-	Case=Dat|Definite=Def|Gender=Masc|Number=Sing|PronType=Art	4	det	_	original_dep=ATR|Ref=544
3	πανώλει	πανώλης	ADJ	a-s---md-	Case=Dat|Gender=Masc|Number=Sing	4	nmod	_	original_dep=ATR|Ref=544
4	πατρὶ	πατήρ	NOUN	n-s---md-	Case=Dat|Gender=Masc|Number=Sing	11	obl	_	original_dep=ADV|Ref=544
5	τῶν	ὁ	DET	l-p---mg-	Case=Gen|Definite=Def|Gender=Masc|Number=Plur|PronType=Art	9	det	_	original_dep=ATR|Ref=544
6	μὲν	μέν	ADV	d--------	PartType=Ptcl	14	advmod	_	original_dep=AuxY|Ref=544
7	ἐξ	ἐκ	ADP	r--------	_	9	case	_	original_dep=AuxP|Ref=544
8	ἐμοῦ	ἐγώ	PRON	p-s---fg-	Case=Gen|Gender=Fem|Number=Sing|Person=1|PronType=Prs	7	nmod	_	original_dep=ATR|Ref=544
9	παίδων	παῖς	NOUN	n-p---mg-	Case=Gen|Gender=Masc|Number=Plur	10	nmod	_	original_dep=ATR|Ref=545
10	πόθος	πόθος	NOUN	n-s---mn-	Case=Nom|Gender=Masc|Number=Sing	11	nsubj	_	original_dep=SBJ|Ref=545
11	παρεῖτο	παρίημι	VERB	v3slie---	Mood=Ind|Number=Sing|Person=3|Voice=MidPass	14	root	_	CoordMember|original_dep=PRED|Ref=545|SpaceAfter=No
12	,	,	PUNCT	u--------	_	14	punct	_	original_dep=AuxX|Ref=545
13	Μενέλεω	Μενέλαος	PROPN	n-s---mg-	Case=Gen|Gender=Masc|Number=Sing	17	nmod	_	original_dep=ATR|Ref=545
14	δ'	δέ	ADV	d--------	PartType=Ptcl	1	cc	_	original_dep=COORD|Ref=545
15	ἐνῆν	ἐνειμί	VERB	v3siia---	Mood=Ind|Number=Sing|Person=3|Tense=Imp|Voice=Act	14	root	_	CoordMember|original_dep=PRED|Ref=545|SpaceAfter=No
16	;	;	PUNCT	u--------	_	0	punct	_	original_dep=AuxK|Ref=545
17	[0]	_	_	_	_	18	nmod	_	NodeType=Artificial|original_dep=ATR
18	[1]	_	_	_	_	15	nsubj	_	NodeType=Artificial|original_dep=SBJ
'''

conll_ita = '''# generator = UDPipe 2, https://lindat.mff.cuni.cz/services/udpipe
# udpipe_model = italian-isdt-ud-2.6-200830
# sent_id = 1
# text = Io leggo le tragedie di Sofocle e lei di Euripide. [0] [1]
1	Io	io	PRON	PE	Number=Sing|Person=1|PronType=Prs	2	SBJ	_	TokenRange=0:2
2	leggo	leggere	VERB	V	Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin	7	PRED_CO	_	TokenRange=3:8
3	le	il	DET	RD	Definite=Def|Gender=Fem|Number=Plur|PronType=Art	4	ATR	_	TokenRange=9:11
4	tragedie	tragedia	NOUN	S	Gender=Fem|Number=Plur	2	OBJ	_	TokenRange=12:20
5	di	di	ADP	E	_	4	AuxP	_	TokenRange=21:23
6	Sofocle	Sofocle	PROPN	SP	_	5	ATR	_	TokenRange=24:31
7	e	e	CCONJ	CC	_	0	COORD	_	TokenRange=32:33
8	lei	lei	PRON	PE	Number=Sing|Person=3|PronType=Prs	12	SBJ	_	TokenRange=34:37
9	di	di	ADP	E	_	13	AuxP	_	TokenRange=38:40
10	Euripide	Euripide	PROPN	SP	_	9	ATR	_	TokenRange=41:49
11	.	.	PUNCT	u--------	_	0	punct	_	_
12	[0]	_	_	_	_	7	PRED_CO	_	NodeType=Artificial
13	[1]	_	_	_	_	12	OBJ	_	NodeType=Artificial|original_dep=SBJ

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

    # writer.apply_on_document(doc)

    # Converter
    converter = SubTreeConverter(with_enhanced=True)
    converter.apply_on_document(doc)

    print(len(tree.empty_nodes))

    # Writer
    writer.apply_on_document(doc)


if __name__ == '__main__':
    main()
