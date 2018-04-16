import unittest
import doctest
import random
import generate

from pprint import pprint

from hypothesis import given
from hypothesis.strategies import dictionaries, lists, text, one_of, just, randoms

class TestToStats(unittest.TestCase):
    @given(dictionaries(one_of(just('>'),
                               just('!'),
                               just(' ')),
                        lists(text(),
                              min_size=0,
                              max_size=100)),
           randoms())
    def test_to_stats(self, d, r):
        desired = {}
        for k, v in d.items():
            if len(v) > 0 and k != ' ':
                desired[k] = len(v)

        temp = []
        for k, v in d.items():
            for e in v:
                temp.append((k, e))

        r.shuffle(temp)

        result = generate.to_stats(temp)

        self.assertEqual(result, desired)


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests

if __name__ == '__main__':
    unittest.main()
