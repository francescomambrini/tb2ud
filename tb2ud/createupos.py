"""Generates the UD Upos based on the AGLDT morphological annotation.
It presupposes a CoNLL representation where the AGLDT postag is stored in the node.xpos

"""

from udapi.core.block import Block


parts = ['ἆρα', 'αὖ', 'γάρ', 'γε', 'γοῦν', 'δή', 'εἶτα', 'καίπερ',
             'καίτοι', 'μά', 'μέν', 'μέντοι', 'μήν', 'μῶν',
             'οὖν', 'ποθι', 'περ', 'ποτέ', 'πού', 'πω', 'τοίνυν', 'τοι', 'τοιγάρ',
             'ἀτάρ', 'ἄν', 'ἄν1', 'ἄρα', 'ἆρα', 'ἤτοι', 'ἦ']

cord_conjs =  ['-δέ', '-τε', 'δέ', 'εἴτε', 'εἶτα', 'ἤ1', 'ἤ', 'ἠέ1', 'καί', 'καίτοι', 'καί', 'μέντοι', 'μήτε', 'μηδέ', 'οὐδέ',
         'οὐδέ', 'οὐδέ', 'οὔτε', 'τε', 'ἀλλά', 'ἀλλά', 'ἠδέ', 'ἠδέ1',  'ἤτε1', 'ἰδέ', 'ἰδέ1', 'ἔπειτα']

dets = ['αὐτός',  'ἀλλήλων', 'ἄλλος',
 'ἐκεῖνος', 'ἐμαυτοῦ', 'ἐμός', 'ἑαυτοῦ', 'ἑκάτερος', 'ἕκαστος',
 'ἡλίκος', 'ἡμέτερος',
 'μηδείς', 'μηδέτερος',
 'νωΐτερος', 'ὁ', 'ὁπηλίκος', 'ὁποῖος', 'ὁπόσος', 'ὁπότερος', 'ὅδε', 'ὅσος',
 'ὅστις', 'οἷος', 'οὐδείς', 'οὐδέτερος', 'οὗτος',
 'πηλίκος', 'ποιός', 'ποσός', 'ποῖος', 'πόσος', 'πότερος', 'πᾶς',
 'σαυτοῦ', 'σφέτερος', 'σός', 'τεός',
 'τήλικος', 'τίς', 'τηλικοῦτος', 'τηλικόσδε', 'τις', 'τοιοῦτος', 'τοιόσδε',
 'τοσοῦτος', 'τοσόσδε', 'τοῖος', 'τόσος',
 'ὑμέτερος']



class CreateUpos(Block):

    def process_node(self, node):

        # sometimes τε is tagged as 'd'
        if node.lemma == 'τε':
            node.xpos = 'c--------'

        newupos = 'X'
        if node.xpos[0] == "a":
            newupos = "ADJ"
        elif node.xpos[0] == 'l':
            newupos = 'DET'
        elif node.xpos[0] == 'i':
            newupos = 'INTJ'
        elif node.xpos[0] == 'r':
            if 'AuxP' in node.deprel:
                newupos = 'ADP'
            else:
                newupos = 'ADV'
        elif node.xpos[0] == 'p':
            newupos = "PRON"
        elif node.xpos[0] in ["d"]:
            newupos = "ADV"
        elif node.xpos[0] == 'g':
            if node.lemma in cord_conjs:
                newupos = 'CCONJ'
            else:
                newupos = 'ADV'
        elif node.xpos[0] == "n":
            if node.form.istitle():
                newupos = "PROPN"
            else:
                newupos = 'NOUN'
        elif node.xpos[0] == 'u':
            newupos = 'PUNCT'
        elif node.xpos[0] == 'c':
            if node.lemma in cord_conjs:
                newupos = "CCONJ"
            else:
                newupos = 'SCONJ'
        elif node.xpos[0] in ['v', 't']:
            if node.deprel == "AuxV":
                newupos = "AUX"
            else:
                newupos = "VERB"

        if node.lemma in dets:
            newupos = 'DET'
        if node.misc["NodeType"] == 'Artificial':
            newupos = '_'

        node.upos = newupos
