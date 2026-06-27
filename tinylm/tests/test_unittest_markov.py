import unittest

import tinylm as mc

class TestMarkov(unittest.TestCase):
    def setUp(self) -> None:
        self.model = mc.Markov("abc")

    def test_predict_deterministic(self) -> None:
        self.assertEqual(self.model.predict("a"), "b")
        self.assertEqual(self.model.predict("b"), "c")

    def test_predict_unknown_raises_keyerror(self) -> None:
        with self.assertRaises(KeyError):
            self.model.predict("z")

            