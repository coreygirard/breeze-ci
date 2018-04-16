import unittest
import doctest
import re
from hypothesis import given
from hypothesis.strategies import one_of, just, integers, from_regex
import render


class TestMakeLineCodeSpan(unittest.TestCase):
    @given(one_of(just('>'),
                  just('!'),
                  just(' ')),
           from_regex(r'\A[a-zA-Z0-9]*\Z'),
           from_regex(r'\A[a-zA-Z0-9]*\Z'))
    def test_make_line_code_span(self, status, code, url):
        line = render.make_line_code_span(status, code, url)
        #print(line)
        #print()
        #self.assertEqual(line.count('/'), 10)

class TestMakeLinkUrl(unittest.TestCase):
    @given(from_regex(r'\A[a-zA-Z0-9]+\Z'),
           from_regex(r'\A[a-zA-Z0-9]+\Z'),
           from_regex(r'\A[a-zA-Z0-9]+\Z'),
           from_regex(r'\A[a-zA-Z0-9]+\Z'),
           integers(min_value=0))
    def test_make_link_url(self, user, repo, hash_, filepath, line_num):
        data = {'user': user,
                'repo': repo,
                'hash': hash_,
                'filepath': filepath,
                'line_num': line_num}
        line = render.make_link_url(data)

        # make sure we're treating hashes properly
        self.assertEqual(line.count('#'), 1)

        # make sure we're not inserting or deleting slashes
        self.assertEqual(line.count('/'),
                         render.make_link_url({k: '' for k in data.keys()}).count('/'))


class TestMakeLineNumSpan(unittest.TestCase):
    @given(integers(min_value=0),
           integers(min_value=0))
    def test_make_line_num_span(self, i, j):
        data = {'line_num': i,
                'max_line_num': i + j}

        result = render.make_line_num_span(data)

        self.assertEqual(result.count('<'), 2)
        self.assertEqual(result.count('>'), 2)

        inner = re.search(r'>([^<]*)<', result)
        self.assertTrue(inner is not None)
        inner = inner.groups()[0]
        inner = inner.replace(' ', '')
        inner = inner.replace('&nbsp', ' ')

        self.assertEqual(inner.strip(), str(i))
        self.assertEqual(len(str(i + j)) + 1,
                         len(inner))
        self.assertEqual(inner[-1], ' ')



def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(render))
    return tests

if __name__ == '__main__':
    unittest.main()
