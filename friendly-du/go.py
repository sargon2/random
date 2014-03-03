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

def make_tabs(output):
    ret = ""
    for item in output:
        ret += "\t".join([str(x) for x in item]) + "\n"
    return ret

def parse(du_output):
    # converts sizes to ints, sorts
    ret = []
    for line in du_output.splitlines():
        (size, item) = line.split()
        ret.append((int(size), item))
    return sorted(ret, key=lambda tup: tup[0], reverse=True)


def doit(num_items, du_output):
    du_output = parse(du_output)
    if num_items == 1:
        output = [du_output[0]]
    if num_items == 2:
        biggest = du_output[1]
        etc_size = du_output[0][0] - biggest[0]
        output = [biggest, (etc_size, './<etc>')]
    if num_items == 3:
        biggest = du_output[1]
        second_biggest = du_output[2]
        etc_size = du_output[0][0] - biggest[0] - second_biggest[0]
        output = [biggest, second_biggest, (etc_size, './<etc>')]
    return make_tabs(output)

class TestDu(unittest2.TestCase):

    def assert_result(self, expected_output, num_items, mock_du_result):
        result = doit(num_items, mock_du_result)
        self.assertEquals(expected_output, result)

    def test_one_file_total(self):
        mock_du_result = "26\t./file1\n30\t.\n"
        expected_output = "30\t.\n"
        self.assert_result(expected_output, 1, mock_du_result)

    def test_one_file_total_fail(self):
        mock_du_result = "26\t./file1\n30\t.\n"
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
        mock_du_result = "20\t./file1\n20\t./file2\n44\t.\n"
        expected_output = "20\t./file1\n24\t./<etc>\n"
        self.assert_result(expected_output, 2, mock_du_result)

    def test_two_files_two_returns_other_order(self):
        mock_du_result = "44\t.\n20\t./file1\n20\t./file2\n"
        expected_output = "20\t./file1\n24\t./<etc>\n"
        self.assert_result(expected_output, 2, mock_du_result)

    def test_two_files_two_returns_different(self):
        mock_du_result = "40\t./file3\n30\t./file4\n88\t.\n"
        expected_output = "40\t./file3\n48\t./<etc>\n"
        self.assert_result(expected_output, 2, mock_du_result)

    def test_two_returns_first_not_biggest(self):
        mock_du_result = "30\t./file3\n40\t./file4\n88\t.\n"
        expected_output = "40\t./file4\n48\t./<etc>\n"
        self.assert_result(expected_output, 2, mock_du_result)

    def test_two_returns_three_items(self):
        mock_du_result = "54\t.\n20\t./file1\n20\t./file2\n10\t./file3\n"
        expected_output = "20\t./file1\n34\t./<etc>\n"
        self.assert_result(expected_output, 2, mock_du_result)

    def test_three_returns_three_items(self):
        mock_du_result = "54\t.\n20\t./file1\n20\t./file2\n10\t./file3\n"
        expected_output = "20\t./file1\n20\t./file2\n14\t./<etc>\n"
        self.assert_result(expected_output, 3, mock_du_result)

    def test_two_returns_deep_folders(self):
        mock_du_result = "24\t./folder1\n34\t./folder2\n20\t./folder1/file1\n30\t./folder2/file2\n62\t.\n"
        expected_output = "34\t./folder2\n28\t./<etc>\n"
        self.assert_result(expected_output, 2, mock_du_result)

    def test_two_folders_four_files(self):
        mock_du_result = "50\t./folder1/file1\n" + \
                         "10\t./folder1/file2\n" + \
                         "60\t./folder2/file1\n" + \
                         "15\t./folder2/file2\n" + \
                         "68\t./folder1\n" + \
                         "83\t./folder2\n" + \
                         "155\t.\n"

        expected_output = "155\t.\n"
        self.assert_result(expected_output, 1, mock_du_result)

        expected_output = "83\t./folder2\n72\t./<etc>\n"
        self.assert_result(expected_output, 2, mock_du_result)

        expected_output = "??"
        self.assert_result(expected_output, 3, mock_du_result)

        expected_output = "??"
        self.assert_result(expected_output, 4, mock_du_result)

    def test_two_folders_four_files_second_folder_small(self):
        mock_du_result = "50\t./folder1/file1\n" + \
                         "60\t./folder1/file2\n" + \
                         "10\t./folder2/file1\n" + \
                         "15\t./folder2/file2\n" + \
                         "114\t./folder1\n" + \
                         "29\t./folder2\n" + \
                         "147\t.\n"

        expected_output = "147\t.\n"
        self.assert_result(expected_output, 1, mock_du_result)

        expected_output = "114\t./folder1\n33\t./<etc>\n"
        self.assert_result(expected_output, 2, mock_du_result)

        expected_output = "60\t./folder1/file2\n54\t./folder1/<etc>\n33\t./<etc>\n"
        self.assert_result(expected_output, 3, mock_du_result)

        expected_output = "??"
        self.assert_result(expected_output, 4, mock_du_result)

    def xtest_three_returns_two_etc(self):
        self.fail("Not written yet")


# Untested.
if __name__ == "__main__":
    print doit(2, run_command("du -a"))
