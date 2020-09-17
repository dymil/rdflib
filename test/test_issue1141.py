import unittest
from io import BytesIO

from rdflib import Graph
from rdflib.plugins.stores.memory import Memory, SimpleMemory
from rdflib.plugins.stores.auditable import AuditableStore


class TestIssue1141(unittest.TestCase):
    """
    Tests is Turtle and TriG parsing works with a store with or without formula support
    """
    def test_issue_1141_1(self):
        file = b"@prefix : <http://example.com/> . :s :p :o ."

        for format in ("turtle", "trig"):
            # with formula
            graph = Graph()
            self.assertTrue(graph.store.formula_aware)
            graph.parse(BytesIO(file), format=format)
            self.assertEqual(len(graph), 1)

            # without
            graph = Graph(store=AuditableStore(Memory()))
            self.assertFalse(graph.store.formula_aware)
            graph.parse(BytesIO(file), format=format)
            self.assertEqual(len(graph), 1)

    def test_issue_1141_2(self):
        file = b"@prefix : <http://example.com/> . :s :p :o ."

        graph = Graph(store=Memory())
        self.assertTrue(graph.store.formula_aware)
        graph.parse(BytesIO(file), format="turtle")
        self.assertEqual(len(graph), 1)

        # without
        graph = Graph(store=SimpleMemory())
        self.assertFalse(graph.store.formula_aware)
        graph.parse(BytesIO(file), format="turtle")
        self.assertEqual(len(graph), 1)
