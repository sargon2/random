#!/usr/bin/python
import sys
header = '#!/usr/bin/python\nimport sys\nheader = '
footer = '\nsys.stdout.write(header + repr(header) + "\\nfooter = " + repr(footer) + footer)\n'
sys.stdout.write(header + repr(header) + "\nfooter = " + repr(footer) + footer)
