try:
    import unittest2 as unittest
except ImportError:
    import unittest

from iscool_e.pynba.collector import Timer

class TimerTestCase(unittest.TestCase):
    def test_timer(self):
        def runner(timer):
            self.assertFalse(timer.started)
            self.assertEqual(timer.elapsed, None)

            with self.assertRaises(RuntimeError):
                timer.stop()

            timer.start()
            self.assertEqual(timer.elapsed, None)
            self.assertTrue(timer.started)
            with self.assertRaises(RuntimeError):
                timer.start()

            timer.stop()
            self.assertFalse(timer.started)
            self.assertIsInstance(timer.elapsed, float)

            self.assertEqual(timer.tags, {'foo': 'bar'})

        timer = Timer(foo="bar")

        runner(timer)

        cloned = timer.clone()
        self.assertIsNot(timer, cloned)

        runner(cloned)

    def test_timer_context(self):
        timer = Timer(foo="bar")
        self.assertFalse(timer.started)
        with timer as t:
            self.assertIs(timer, t)
            self.assertTrue(t.started)

        self.assertIs(timer, t)
        self.assertFalse(t.started)

    def test_timer_decorator(self):
        def runner():
            return

        timer = Timer(foo="bar")
        decorated = timer(runner)
        decorated()

    def test_timer_repr(self):
        timer = Timer(foo="bar")
        assert 'Timer' in repr(timer)
        timer.start()
        assert 'started:' in repr(timer)
        timer.stop()
        assert 'elapsed:' in repr(timer)
