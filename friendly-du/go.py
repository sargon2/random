#!/usr/bin/python
import unittest2
import subprocess

# The idea here is we list the N largest items in the given folder.
# e.g.:
# <size> Files in . except those listed below
# <size> ./folder1 except those listed below
# <size> ./folder1/folder2
# <size> ./folder3 # has many folder in it, but they're small individually, so we don't list them here

# Maybe ./folder1/<etc> or something is better wording.

def run_command(command):
    return subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]

class TestDu(unittest2.TestCase):
    def doit(self, num_levels, du_output):
        for line in du_output.splitlines():
            (size, item) = line.split()
            if item == '.' and num_levels == 1:
                return "%s\t%s\n" % (size, item)
        return "2"

    def assert_result(self, expected_output, num_levels, mock_du_result):
        result = self.doit(num_levels, mock_du_result)
        self.assertEquals(expected_output, result)

    def test_one_file_total(self):
        mock_du_result = "26\t./file1\n30\t.\n"
        expected_output = "30\t.\n"
        self.assert_result(expected_output, 1, mock_du_result)

    def test_one_file_total_fail(self):
        mock_du_result = "26\t./file1\n.\t30"
        expected_output = "26\t.\n"
        with self.assertRaises(AssertionError):
            self.assert_result(expected_output, 1, mock_du_result)

    def test_one_file_total_different(self):
        mock_du_result = "36\t./file1\n40\t.\n"
        expected_output = "40\t.\n"
        self.assert_result(expected_output, 1, mock_du_result)

    def test_two_files(self):
        mock_du_result = "20\t./file1\n20\t./file2\n44\t.\n"
        expected_output = "44\t.\n"
        self.assert_result(expected_output, 1, mock_du_result)

    def test_two_files_two_returns(self):
        mock_du_result = "./file1\t20\n./file2\t20\n.\t44"
        expected_output = "./file1\t20\n./<etc>\t24\n"
        self.assert_result(expected_output, 2, mock_du_result)

    def test_two_files_two_returns_other_order(self):
        mock_du_result = ".\t44\n./file2\t20\n./file1\t20\n"
        expected_output = "./file1\t20\n./<etc>\t24\n"
        self.assert_result(expected_output, 2, mock_du_result)

    def test_two_files_two_returns_different(self):
        mock_du_result = "./file3\t40\n./file4\t30\n.\t88\n"
        expected_output = "./file3\t40\n./<etc>\t48\n"
        self.assert_result(expected_output, 2, mock_du_result)


# Untested.
if __name__ == "__main__":
    pass
