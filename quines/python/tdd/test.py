import unittest2
import subprocess

class TestQuine(unittest2.TestCase):
    def test_is_quine(self):
        filename = "./quine.py"
        result = subprocess.check_output(filename, shell=True)
        with open(filename) as f:
            src = f.read()
            print "Output:"
            print result
            print
            print "Source:"
            print src
            self.assertEquals(result, src)
