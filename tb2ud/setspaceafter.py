'''Set SpaceAfter=No in the MISC field for all the intra-word tokenized elements.

These words include:
- compound conjunctions: εἴτε, μήτε, μηδέ, οὐδέ, οὔτε
- krasis

NOTE THAT: some Perseus-compliant projects (e.g. Gorman) tokenize the intra-word
elements adding an hyphen (e.g. "κ-", "ἀγὼ"); this case is regulated with a dedicated
script that takes care not only to set the SpaceAfter property, but also to delete
the hyphen from the word form.
'''

from udapi.core.block import Block
import re

conj_pattern = r'''^εἴ(τε|[τθ][᾽'])$  # conjunctions: εἴτε
            | ^(μη|μή|οὐ)(τε\b|δ[έὲ]\b|[τδθ][᾽'])$      #
            '''

conj_reg = re.compile(conj_pattern,
            flags=re.UNICODE | re.MULTILINE | re.DOTALL | re.VERBOSE)


punct = [',', '·', ';', '.']

class SetSpaceAfter(Block):

    def _is_krasis(self, node):
        reg = re.compile(r'^[κχ]-?$')
        if reg.search(node.form):
            return True
        return False

    def _is_lemmatized_conj(self, node):
        """Check whether the two chunks of the compound conjunction are lemmatized
        under the right lemma of the cojunction; in that case, return True for the
        first part.
        """
        conjs = ['εἴτε', 'μήτε', 'μηδέ', 'οὐδέ', 'οὔτε']
        if node.lemma in conjs:
            n = node.next_node
            if n:
                if n.lemma == node.lemma:
                    return True
        return False

    def _is_compound_cojn(self, node):
        """Returns true only if first-element in a compound conjunction
        (εἴτε, μήτε, μηδέ, οὐδέ, οὔτε)
        """
        nf = ""
        if node.next_node:
            nf = node.next_node.form
        concat = node.form + nf
        if conj_reg.search(concat):
            return True
        return False

    def _is_hyphenated_conj(self, node):
        if node.next_node:
            nf = node.next_node.form
            nl = node.next_node.lemma
            if nf[0] == '-' and nl in ['δέ', 'τε']:
                return True
        return False



    def _followed_by_punct(self, node):
        if node.next_node:
            nf = node.next_node.form
            if nf in punct:
                return True
        return False

    def process_tree(self, tree):
        for node in tree.descendants:
            nospace = False
            # if SpaceAfter is already set, do nothing
            if node.misc['SpaceAfter'] == 'No':
                continue
            else:
                if node.form in ['[', '(']:
                    nospace = True
                # In Tragedy, a single quote as token is generally the product of prodelision
                # e.g. ἐγὼ ' φύλαξα < ἐγὼ 'φύλαξα < ἐγὼ ἐφύλαξα, so no space after.
                # Warning! Other tokenizers may behave differently...
                elif node.form == "'":
                    nospace = True
                if self._followed_by_punct(node):
                    nospace = True
                if self._is_hyphenated_conj(node):
                    nospace = True
                if self._is_krasis(node):
                    nospace = True
                elif self._is_lemmatized_conj(node):
                    nospace = True
                elif self._is_compound_cojn(node):
                    nospace = True
            if nospace:
                node.misc['SpaceAfter'] = 'No'

        # Now we re-compute the text with the new SpaceAfter values
        txt = tree.compute_text()
        tree.text = txt
