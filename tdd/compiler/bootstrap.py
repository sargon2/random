import unittest2
import os
import shutil

def make_compiler(target):
    shutil.copy("./bootstrap-compiler.py", target)

    # Do the bootstrap; after this, every bit in the compiler was written in the new language
    os.system("./compile -o ./compile compiler-source.newlang") # TODO: newlang is a terrible extension

def mycompile(code):
    with open("to_compile", "w") as f:
        f.write(code)
    os.system("./compile -o compiled to_compile")
    return "./compiled"

def execute(exename):
    return os.system(exename)

def compile_and_run(code):
    exename = mycompile(code)
    return execute(exename)

class TestCompilerBootstrap(unittest2.TestCase):

    def setUp(self):
        make_compiler("./compile")

    def tearDown(self):
        to_remove = ["./to_compile", "./compile", "./compiled"]
        for item in to_remove:
            try:
                os.remove(item)
            except:
                pass

    def test_assert_equals(self):
        self.assertEquals(0, compile_and_run("assertEquals(1, 1)"))
        self.assertEquals(1, compile_and_run("assertEquals(1, 2)"))
