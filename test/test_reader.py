import unittest
import os
import tb2ud

from udapi.core.root import Root
from udapi.core.node import Node, find_minimal_common_treelet
from udapi.core.document import Document
from udapi.block.read.agldt import Agldt as AgldtReader
from udapi.block.write.conllu import Conllu as ConlluWriter


class TestEnhDeps(unittest.TestCase):
    """Unit tests for udapi.core.node and enhanced dependecies.
    Tests the behaviour with empty nodes (with decimal ord, such as 0.1, 2.3 etc.) as well"""

    @classmethod
    def setUpClass(cls):
        cls.doc = Document()
        cls.data = os.path.join(os.path.dirname(tb2ud.__file__), "../test/data/tlg0011.tlg005.daphne_tb-grc1.xml")
        reader = AgldtReader(cls.data)
        reader.apply_on_document(cls.doc)
        print(len(cls.doc.bundles))
        cls.tree = cls.doc.bundles[263].get_tree()
        cls.nodes = cls.tree.descendants

    def test_load_data(self):
        self.assertEqual(929, len(self.doc.bundles))

    def test_sentence(self):
        self.assertEqual(16, len(self.nodes))
        self.assertEqual("ἢ", self.nodes[0].form)
