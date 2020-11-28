import unittest
import os
import tb2ud
import logging

from udapi.core.document import Document
from udapi.block.read.conllu import Conllu as ConlluReader
from udapi.block.write.conllu import Conllu as ConlluWriter
from tb2ud.subtreeconverter import SubTreeConverter
from tb2ud.shiftartificials import ShiftArtificials

logging.basicConfig(level=logging.DEBUG)


class TestEnhDeps(unittest.TestCase):
    """Unit tests for udapi.core.node and enhanced dependecies.
    Tests the behaviour with empty nodes (with decimal ord, such as 0.1, 2.3 etc.) as well"""

    @classmethod
    def setUpClass(cls):
        cls.doc = Document()
        cls.data = os.path.join(os.path.dirname(tb2ud.__file__), "../test/data/artificials.conllu")
        cls._reader = ConlluReader(files=cls.data)
        cls._reader.apply_on_document(cls.doc)
        # cls.tree = cls.doc.bundles[0].get_tree()
        # cls.nodes = cls.tree.descendants
        cls.writer = ConlluWriter()
        cls._subtreeconverted = False

    def apply_converter(self):
        if not self._subtreeconverted:
            shifter = ShiftArtificials()
            converter = SubTreeConverter(with_enhanced=True)
            shifter.apply_on_document(self.doc)
            converter.apply_on_document(self.doc)
            self._subtreeconverted = True
        else:
            logging.debug("I am not redoing the conversion...")

    def test_reading(self):
        tree = self.doc.bundles[0].get_tree()
        self.assertEqual('Artificial', tree.descendants[-1].misc['NodeType'])

    def test_subtree_conversion(self):
        self.apply_converter()
        empties = self.doc.bundles[2].get_tree().empty_nodes
        self.assertEqual(len(empties), 2)

        #self.writer.apply_on_document(self.doc)

    def test_write_converted(self):
        #self.apply_converter()
        writer = ConlluWriter(files='test_artificial_deps.conllu')
        writer.apply_on_document(self.doc)
