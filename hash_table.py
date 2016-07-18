import unittest2

class KeyValue(object):
    def __init__(self, key, val):
        self._key = key
        self._val = val

    def has_key(self):
        return True

    def key(self):
        return self._key

    def value(self):
        return self._val

    def __str__(self):
        return "" + str(self._key) + " : " + str(self._val)

class NoValue(object):
    def has_key(self):
        return False

    def value(self):
        raise MissingValueException()

class hash_table(object):
    def __init__(self):
        self.vals = [NoValue()]

    def put(self, key, val):
        index = self.get_index(key)
        current_keyval = self.vals[index]
        if current_keyval.has_key() and current_keyval.key().__hash__() != key.__hash__():
            self.resize()
            return self.put(key, val)
        self.vals[index] = KeyValue(key, val)

    def resize(self):
        current_size = len(self.vals)
        old_vals = self.vals
        self.vals = [NoValue()] * current_size * 2
        for item in old_vals:
            if item.has_key():
                self.put(item.key(), item.value())

    def get_index(self, key):
        return key.__hash__() % len(self.vals)

    def get(self, key):
        index = self.get_index(key)
        return self.vals[index].value()

class MissingValueException(Exception):
    pass

class TestHashTable(unittest2.TestCase):
    def assert_put_get(self, key, val):
        h = hash_table()
        h.put(key, val)
        self.assertEquals(val, h.get(key))

    def test_put_get(self):
        self.assert_put_get("a", 1)
        self.assert_put_get(1, "a")
        self.assert_put_get("b", 2)
        self.assert_put_get("a", None)
        self.assert_put_get(None, 1)
        self.assert_put_get(None, None)

    def test_put_two(self):
        h = hash_table()
        h.put("a", 1)
        h.put("b", 2)
        self.assertEquals(1, h.get("a"))
        self.assertEquals(2, h.get("b"))

    def test_dne(self):
        h = hash_table()
        with self.assertRaises(MissingValueException):
            h.get("a")

    def test_overwrite(self):
        h = hash_table()
        h.put("a", 1)
        h.put("a", 2)
        self.assertEquals(2, h.get("a"))

    def test_many_values(self):
        h = hash_table()
        for i in xrange(1, 100):
            h.put(i, i)
        for i in xrange(1, 100):
            self.assertEquals(i, h.get(i))

    def test_speed(self):
        h = hash_table()
        for i in xrange(1, 100000):
            h.put(i, i)
