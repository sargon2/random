
import resource

with open('/usr/share/dict/words') as f:
    for line in f:
        add_word(line.strip())

print str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) + "kb ram used"
