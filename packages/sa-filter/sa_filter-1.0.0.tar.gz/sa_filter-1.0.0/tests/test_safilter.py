# -*- coding: utf-8 -*-

import unittest

import pandas as pd

from sa_filter import SAFilter


class TestSAFilter(unittest.TestCase):

    def setUp(self) -> None:
        # these just stop on the first filter
        self.mols_lint = [
            ('C1N=C1', 'aziridine-like N in 3-membered ring > 0'),
            ('NN=N', 'acyclic N-,=N and not N bound to carbonyl or sulfone > 0'),
        ]

    def test_lint(self):
        safilter = SAFilter()
        result = pd.DataFrame.from_records(safilter.contains_alert(list(zip(*self.mols_lint))[0],
                                                                   return_alerts=True),
                                           columns=['is_alert', 'set', 'description'])
        # Test boolean result
        self.assertListEqual(result.is_alert.tolist(), [False if x == 'OK' else True for _, x in self.mols_lint])
