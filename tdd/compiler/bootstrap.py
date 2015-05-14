import unittest2
import os
import shutil
import subprocess

def make_compiler(target):
    shutil.copy("./bootstrap-compiler.py", target)

    # Do the bootstrap; after this, every bit in the compiler was written in the new language
    subprocess.check_call(target + " -o new-compiler compiler-source.newlang", shell=True) # TODO: newlang is a terrible extension
    shutil.move("new-compiler", target)

    # Compile again for verification
    subprocess.check_call(target + " -o verify compiler-source.newlang", shell=True)
    subprocess.check_call("diff " + target + " verify", shell=True)

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

    def tearDown(self):
        to_remove = ["./to_compile", "./compile", "./compiled", "./verify"]
        for item in to_remove:
            try:
                os.remove(item)
            except:
                pass

    def test_assert_equals(self):
        make_compiler("./compile")
        self.assertEquals(0, compile_and_run("assertEquals(1, 1)"))
        self.assertEquals(1, compile_and_run("assertEquals(1, 2)"))
