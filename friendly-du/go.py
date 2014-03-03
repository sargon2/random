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

# First, get an overall size.
# Then, recurse, and at each level, either return the current folder, or split it and recurse further.
# We can only "split" one item off -- no "<size> folder1 and folder2" or anything like that.

# Maybe I should have a split() function that takes in a folder, finds the largest unsplit item, and splits it.
# Then I could just call it N times.

def run_command(command):
    ''' Why is this so hard? '''
    return subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]

class real_du_provider(object):
    ''' Untested. '''
    def get_du(self, path):
        command = "du -sk %s" % (path)
        return int(run_command(command).split()[0])
    def get_du_for_children(self, path):
        command = "du -sk %s/*" % (path)
        r = run_command(command)
        ret = {}
        for item in r.splitlines():
            (size, item) = item.split()
            ret[item] = int(size)
        return ret

def du(num_items, du_provider=None):
    if not du_provider:
        du_provider = real_du_provider()
    items = DuResult(du_provider, '.')
    while(len(items) < num_items):
        items = items.split()
    return items.dict()

class DuResult(object):
    def __init__(self, provider, initial_item = None):
        self.provider = provider
        self.sizes_dict = {}
        if initial_item is not None:
            self.sizes_dict[initial_item] = provider.get_du(initial_item)

    def __len__(self):
        return len(self.sizes_dict)

    def dict(self):
        return self.sizes_dict

    def get_largest(self, dict=None):
        if dict is None:
            dict = self.sizes_dict
        max = None
        ret = None
        for key, value in dict.iteritems():
            if max is None or max < value:
                ret = key
                max = value
        return ret

    def sum(self, dict):
        return sum(dict.values())

    def split(self):
        largest = self.get_largest()
        inner_result = self.provider.get_du_for_children(largest)
        inner_largest = self.get_largest(inner_result)
        new_dict = {}
        inner_largest_size = inner_result[inner_largest]
        new_dict[inner_largest] = inner_largest_size
        new_dict[largest + "/<etc>"] = self.sizes_dict[largest] - inner_largest_size

        ret = DuResult(self.provider)
        ret.sizes_dict = new_dict
        return ret

class TestDu(unittest2.TestCase):
    def mock_du_provider(self, mock_fs):
        class provider(object):
            def __init__(self, mock_fs):
                self.mock_fs = mock_fs
            def get_du(self, path):
                return self.mock_fs.get(path)
            def get_du_for_children(self, path):
                # Ugh.  Mocking.
                ret = {}
                for key, value in self.mock_fs.iteritems():
                    if key == path:
                        continue
                    ret[key] = value
                return ret
        return provider(mock_fs)

    def assert_result(self, expected_output, num_items, mock_fs):
        # mock_fs is the simulated result if you run "du -sk <key>"
        actual_output = du(num_items, du_provider=self.mock_du_provider(mock_fs))
        self.assertEquals(expected_output, actual_output)

    def test_one_file_total(self):
        mock_fs = { ".": 30,
                    "./file1": 26 }
        self.assert_result({".": 30}, 1, mock_fs)

    def test_one_file_total_fail(self):
        mock_fs = { ".": 30,
                    "./file1": 26 }
        with self.assertRaises(AssertionError):
            self.assert_result({".": 26}, 1, mock_fs)

    def test_one_file_total_different(self):
        mock_fs = { ".": 40,
                    "./file1": 36 }
        self.assert_result({".": 40}, 1, mock_fs)

    def test_two_files(self):
        mock_fs = { ".": 44,
                    "./file1": 20,
                    "./file2": 20
                  }
        self.assert_result({".": 44}, 1, mock_fs)

    def test_two_files_two_returns(self):
        mock_fs = { ".": 44,
                    "./file1": 20,
                    "./file2": 20
                  }
        expected_result = { "./file1": 20,
                            "./<etc>": 24
                          }
        self.assert_result(expected_result, 2, mock_fs)

    def test_two_files_two_returns_other_order(self):
        mock_fs = { ".": 44,
                    "./file1": 20,
                    "./file2": 20
                  }
        expected_result = { "./<etc>": 24,
                            "./file1": 20
                          }
        self.assert_result(expected_result, 2, mock_fs)

    def test_two_files_two_returns_different(self):
        mock_fs = { ".": 88,
                    "./file3": 40,
                    "./file4": 30
                  }
        expected_result = { "./file3": 40,
                            "./<etc>": 48
                          }
        self.assert_result(expected_result, 2, mock_fs)


# Untested.
if __name__ == "__main__":
    result = du(10)
    print result
