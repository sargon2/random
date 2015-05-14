#!/usr/bin/env python

import sys
import os

infile = sys.argv[3]
outfile = sys.argv[2]

with open(infile) as f:
    contents = f.read()

# Note that contents is always the same.  So we could just hardcode the output if we wished.

# TODO: this stuff is dup'd with compiler-source.newlang; how do I remove that duplication?
# This one compiles to python and the other could compile to asm or whatever.
# This only has to handle the compiler's code itself; other code (that the compiler handles) isn't important here.
new_contents = "#!/usr/bin/env python\nimport sys\n"
for line in contents.splitlines():

    if line == "chmod(outfile, 0755)":
        line = "import os\nos.chmod(outfile, 0755)"
    if line == "contents = read_file(infile)":
        line = "with open(infile) as f:\n    contents = f.read()\n"
    if line == "write_file(outfile, new_contents)":
        line = "with open(outfile, \"w\") as f:\n    f.write(new_contents)\n"

    new_contents += line + "\n"

with open(outfile, "w") as f:
    f.write(new_contents)

os.chmod(outfile, 0755)
