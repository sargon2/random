import unittest2
import os
import shutil
import subprocess

def mycompile(code):
    with open("to_compile", "w") as f:
        f.write(code)
    subprocess.check_call("./compile -o compiled to_compile", shell=True)
    return "./compiled"

def execute(exename):
    return os.system(exename)

def compile_and_run(code):
    exename = mycompile(code)
    return execute(exename)

class TestCompilerBootstrap(unittest2.TestCase):

    def tearDown(self):
        to_remove = ["./to_compile", "./compiled"]
        for item in to_remove:
            try:
                os.remove(item)
            except:
                pass

    def test_assert_equals(self):
        self.assertEquals(0, compile_and_run("assertEquals(1, 1);"))
        self.assertEquals(0, compile_and_run("assertEquals(1, 1);\nassertEquals(2, 2);"))
        self.assertNotEquals(0, compile_and_run("assertEquals(1, 2);\nassertEquals(2, 2);"))
        self.assertNotEquals(0, compile_and_run("assertEquals(1, 1);\nassertEquals(1, 2);"))
        self.assertNotEquals(0, compile_and_run("assertEquals(1, 2);"))
