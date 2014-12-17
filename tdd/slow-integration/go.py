import unittest2
import time
import os
import pickle

class SlowApi(object):
    def slow_api(self):
        time.sleep(30)
        return 3

class Invoker(object):
    def __init__(self, api):
        self.api = api

    def invoke(self):
        return self.api.slow_api() + 1

class Recorder(object):
    def __init__(self, class_to_record):
        self.class_to_record = class_to_record

    def has_result(self):
        return os.path.isfile("result")

    def remember(self, result):
        with open("result", "w") as f:
            serialized = pickle.dumps(result)
            f.write(serialized)

    def get_result(self):
        with open("result") as f:
            serialized = f.read()
            return pickle.loads(serialized)

    def memoize(self, attribute_name):
        attribute = self.class_to_record.__getattribute__(attribute_name)
        def injected(*args, **kwargs):
            if(self.has_result()):
                result = self.get_result()
            else:
                result = attribute(*args, **kwargs)
                self.remember(result)
            return result
        return injected

    def __getattr__(self, attribute):
        return self.memoize(attribute)

# TODO: more than one api call on the same object
# TODO: multiple values from the same api call (different over time)
# TODO: named recorders that store their values in a folder with their name (multiple apis to call)
# TODO: what if instantiation is slow?
# TODO: what if the slow class overrides __getattribute__ and/or __getattr__?
# TODO: what if the api result depends on a constructor argument?  Does that affect things?
# TODO: what if you call api A, then B, then A, and the second time you call A it's different?
#       The second call to A could be different because B was called, or because it's the second time A was called.
#       The recorder should support both.  The user should choose between them when they write the test. (?)

class TestSomething(unittest2.TestCase):
    def xtest_slow_without_sut(self): # too slow to run
        sut = Invoker(SlowApi())
        self.assertEquals(4, sut.invoke())
    def test_basic_record_and_replay(self):
        recorder = Recorder(SlowApi())
        sut = Invoker(recorder)
        self.assertEquals(4, sut.invoke())
