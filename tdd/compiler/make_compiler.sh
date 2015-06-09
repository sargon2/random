#!/bin/bash -ex

target="$1"
cp "./bootstrap-compiler.py" $target

# Do the bootstrap; after this, every bit in the compiler was written in the new language
$target -o new-compiler compiler-source.newlang # TODO: newlang is a terrible extension
mv new-compiler $target

# Now the new compiler was compiled by the bootstrap compiler.  We want to remove all traces of that, so let's recompile again.
$target -o new-compiler compiler-source.newlang
mv new-compiler $target

# Compile again for verification
$target -o verify compiler-source.newlang
diff $target verify
rm -f verify
