"""Populates the FEATS column based on the AGLDT morphological annotation.
Note that the Tense feat is hardly compatible with the "tense" slot of the guidelines for AGDT, due to the peculiar
nature of what we traditionally call "tense" of Greek verbs, which in UD terms is more a combination of tense and
aspect.
Therefore, it is left empty in most cases. Users interested in retrieving the Greek 'aorists' or 'perfect' should rather query
the 4th position (indexed from 1) of the xpos tag than rely on the Tense feat.
"""


from udapi.core.block import Block
import logging


# Pronouns
pron_dem = ['ἐκεῖνος', 'ὅδε', 'οὗτος', 'τοσόσδε', 'τοιόσδε', 'τηλίκος', 'τηλικοῦτος', 'τηλικόσδε', 'τοιοῦτος',
            'τοῖος', 'τοσοῦτος', 'τόσος']
pron_ind = ['τις', 'ἄλλος', 'ἕκαστος', 'ἑκάτερος', 'πᾶς', 'ποιός', 'ποσός']
pron_int = ['τίς', 'πόσος', 'ποῖος', 'ὁποῖος', 'ὁπόσος', 'πότερος', 'πηλίκος'] # 'ποῦ', 'πῆ', 'πότε', ]
pron_neg = ['οὐδείς', 'οὔτις', 'μηδείς', 'οὐδέτερος', 'μηδέτερος']
pron_per = ['ἕ', 'αὐτός', 'νιν', 'σύ', 'ἐγώ', 'ἐγώγε', 'σφεῖς', 'ἡμεῖς', 'ὑμεῖς']
pron_poss = ['ἐμός', 'ἡμέτερος', 'ἐμός', 'σός', 'ὑμέτερος', 'νωΐτερος', 'σφέτερος']
pron_refl = ['ἐμαυτοῦ', 'σαυτοῦ', 'ἑαυτοῦ', ]
pron_rel = ['ὅστις', 'ὅς', 'ὅσπερ', 'ὅσος', 'οἷος', 'ὁπόσος', 'ὁπότερος', 'ὁπηλίκος', 'ἡλίκος']

# Particles
ptcl = ['ἆρα', 'ἀτάρ', 'αὐτάρ', 'αὖ', 'γάρ', 'γε', 'γοῦν', 'δέ', 'δή', 'δήπου', 'δῆθεν', 'δῆτα', 'εἶτα', 'κάρτα',
        'καίπερ', 'καίτοι', 'μά', 'μάν', 'μέν', 'μέντοι', 'μήν', 'μῶν',
        'οὖν', 'ποθι', 'περ', 'ποτέ', 'πού', 'πω', 'τοίνυν', 'τοι', 'τοιγάρ',
        'ἀτάρ', 'ἄν', 'ἄν1', 'ἄρα', 'ἆρα', 'ἤτοι', 'ἦ']


# TODO: 1. tense and aorist
# TODO: medio/passive, middle, passive...; solutions: PROIEL: mid per dep, Voice=Mid,Pass; Perseus: always Mid

class CreateFeats(Block):
    def process_node(self, node):
        if node.misc["NodeType"] == 'Artificial':
            return None
        if len(node.xpos) > 10:
            newxpos = node.xpos[:9]
            node.xpos = newxpos
            logging.warning(f'{node.form} ({node.address()}): using first 9 position only ({node.xpos} > {newxpos})')
        try:
            _, per, num, tense, mood, voice, gen, case, deg = [t for t in node.xpos]
        except ValueError:
            logging.error(f'{node.form} ({node.address()}): malformed tag ({node.xpos})')
            return None

        # Person feature
        if per in ['1', '2', '3']:
            node.feats["Person"] = per
        else:
            if node.lemma in ['ἐγώ', 'ἡμεῖς']:
                node.feats["Person"] = '1'
            elif node.lemma in ['σύ', 'ὑμεῖς']:
                node.feats["Person"] = '2'

        # Number
        if num == 's':
            node.feats['Number'] = 'Sing'
        elif num == 'p':
            node.feats['Number'] = 'Plur'
        elif num == 'd':
            node.feats['Number'] = 'Dual'

        # Mood
        if mood == 'i':
            node.feats['Mood'] = 'Ind'
        if mood == 's':
            node.feats['Mood'] = 'Sub'
        if mood == 'o':
            node.feats['Mood'] = 'Opt'
        if mood == 'm':
            node.feats['Mood'] = 'Imp'
        # infinitive and participle are not moods but verb forms
        if mood == 'n':
            node.feats['VerbForm'] = 'Inf'
        if mood == 'p':
            node.feats['VerbForm'] = 'Part'

        # Tense
        if tense == 'p':
            node.feats['Tense'] = 'Pres'
        elif tense == 'i':
            node.feats['Tense'] = 'Imp'
        # elif tense == 'r':
        #     node.feats['Tense'] = 'Perf'
        # elif tense == 'l':
        #    node.feats['Tense'] = 'Pqp'
        elif tense == 't':
            node.feats['Tense'] = 'FutPerf'
        elif tense == 'f':
            node.feats['Tense'] = 'Fut'

        # Aorist has tense value only in the past.
        # UD is not equipped to deal with aspectual value of Greek Aorist and Pf
        elif tense == 'a' and node.feats["Mood"] == "Ind":
            node.feats['Tense'] = 'Past'

        # voice
        if voice == 'a':
            node.feats['Voice'] = 'Act'
        if mood == 'p':
            node.feats['Voice'] = 'Pass'
        if voice == 'm':
            node.feats['Voice'] = 'Mid'
        if voice == 'e':
            node.feats['Voice'] = 'MidPass'

        # Gender
        if gen == 'm':
            node.feats['Gender'] = 'Masc'
        if gen == 'f':
            node.feats['Gender'] = 'Fem'
        if gen == 'n':
            node.feats['Gender'] = 'Neut'

        # Case
        if case == 'n':
            node.feats['Case'] = 'Nom'
        if case == 'a':
            node.feats['Case'] = 'Acc'
        if case == 'd':
            node.feats['Case'] = 'Dat'
        if case == 'g':
            node.feats['Case'] = 'Gen'
        if case == 'v':
            node.feats['Case'] = 'Voc'
        if case == 'l':
            node.feats['Case'] = 'Loc'

        # Degree
        if deg == 'c':
            node.feats['Degree'] = 'Cmp'
        if deg == 's':
            node.feats['Degree'] = 'Sup'

        # Additional Features
        # PronType
        if node.lemma == 'ὁ':
            node.feats["PronType"] = 'Art'
            node.feats["Definite"] = 'Def'
        elif node.lemma == 'ἀλλήλων':
            node.feats["PronType"] = 'Rcp'
        elif node.lemma in pron_dem:
            node.feats["PronType"] = 'Dem'
        elif node.lemma in pron_ind:
            node.feats["PronType"] = 'Ind'
        elif node.lemma in pron_dem:
            node.feats["PronType"] = 'Dem'
        elif node.lemma in pron_ind:
            node.feats["PronType"] = 'Ind'
        elif node.lemma in pron_int:
            node.feats["PronType"] = 'Int'
        elif node.lemma in pron_neg:
            node.feats["PronType"] = 'Neg'
        elif node.lemma in pron_rel:
            node.feats["PronType"] = 'Rel'
        elif node.lemma in pron_per:
            node.feats["PronType"] = 'Prs'
        elif node.lemma in pron_poss:
            node.feats["PronType"] = 'Prs'
            node.feats["Poss"] = 'Yes'
        elif node.lemma in pron_refl:
            node.feats["PronType"] = 'Prs'
            node.feats["Reflex"] = 'Yes'

        # Particle type
        # an interesting feature! For the present we mark only the value Ptcl, to signal the fact that words
        # that are tagged as ADV belong in fact to the traditional class of "Greek Particles" of standard grammars
        if node.lemma in ptcl:
            node.feats["PartType"] = "Ptcl"

