import unittest
import doctest

from hypothesis import given, assume
from hypothesis.strategies import text, lists, integers

import increment_pypi

class TestIncrement(unittest.TestCase):
    @given(lists(integers(min_value=0), min_size=1))
    def test_increment(self, e):
        before = '.'.join([str(i) for i in e])
        e[-1] += 1
        after = '.'.join([str(i) for i in e])

        self.assertEqual(increment_pypi.increment(before), after)
        print(before, after)


class TestIncrementVersionNumber(unittest.TestCase):
    @given(text(),
           lists(integers(min_value=0), min_size=1),
           text())
    def test_increment_version_number(self, a, b, c):
        assume("version='" not in a)
        assume("version='" not in c)

        before_b = '.'.join([str(i) for i in b])
        b[-1] += 1
        after_b = '.'.join([str(i) for i in b])

        before_text = a + "version='{0}',".format(before_b) + c
        after_text = a + "version='{0}',".format(after_b) + c
        #test = a + "version='" + new_b + "'," + c
        test = increment_pypi.increment_version_number(before_text)

        self.assertEqual(after_text, test)


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests

if __name__ == '__main__':
    unittest.main()
