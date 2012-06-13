try:
    import unittest2 as unittest
except ImportError:
    import unittest

from iscool_e.pynba.reporter import flattener

class ReporterTestCase(unittest.TestCase):
    def test_flattener(self):
        assert flattener({'foo': 12}) == [('foo', '12')]
        assert flattener({'foo': [12, 13]}) == [('foo', '12'), ('foo', '13')]
        assert flattener({'foo': [12]}) == [('foo', '12')]
        assert flattener({'foo': [12]}) == [('foo', '12')]
        assert flattener({'foo': {'foo': [12]}}) == [('foo.foo', '12')]
        assert flattener({'foo': lambda : ['bar', 'baz']}) == [('foo', 'bar'), ('foo', 'baz')]
        assert flattener({'foo': {42: [12]}}) == [('foo.42', '12')]
