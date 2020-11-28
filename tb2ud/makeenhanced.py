from udapi.core.block import Block
import logging


def _has_deps(tree):
    for n in tree.descendants:
        if n.raw_deps != '_':
            return True


class MakeEnhanced(Block):

    def process_tree(self, tree):
        if _has_deps(tree):
            for n in tree.descendants:
                if n.raw_deps == '_':
                    n.deps.append({'parent': n.parent, 'deprel': n.deprel})
